import os
import re
import time

import oss2
import requests
from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.colors import red
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from tortoise.expressions import Q

from app.controllers.sensitive_word import sensitive_word_controller
from app.core.crud import CRUDBase
from app.models.admin import Crawler
from app.schemas.crawler import CrawlerCreate, CrawlerUpdate
from app.utils.oss_config import OSS_ENDPOINT, OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_BUCKET_NAME


def upload_to_oss(file_path, object_name):
    """
    将文件上传到阿里云OSS。

    Args:
        file_path: 本地文件的路径。
        object_name: 文件在OSS中存储的对象名称。

    Returns:
        上传成功后文件的URL，如果失败则返回None。
    """
    try:
        # 创建Bucket实例
        auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
        # 上传文件
        bucket.put_object_from_file(object_name, file_path)

        # 返回文件的URL
        return f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{object_name}"
    except oss2.exceptions.OssError as e:
        print(f"上传到OSS失败: {e}")
        return None


class CrawlerController(CRUDBase[Crawler, CrawlerCreate, CrawlerUpdate]):
    def __init__(self):
        super().__init__(model=Crawler)

    async def do_crawler(self, crawler_data: CrawlerCreate):
        # 创建新的Crawler实例
        crawler = await self.model.create(**crawler_data.dict())
        # 获取爬虫信息
        url = crawler.url
        method = crawler.method
        params = crawler.params
        headers = crawler.headers
        # 发起请求获取详细页面内容
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers)
            else:
                response = requests.post(url, params=params, headers=headers)

            response.raise_for_status()  # 检查请求是否成功，如果失败则抛出异常

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            # 更新爬虫状态为失败
            crawler.status = 'failed'
            await crawler.save()
            return False

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取标题
            title = soup.select_one('h1.title-article')
            title_text = title.get_text().strip() if title else "标题未找到"

            # 提取文章主体内容
            article = soup.select_one('div#content_views')
            paragraphs = []

            if article:
                # 提取所有段落文本
                for p in article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'pre']):
                    text = p.get_text().strip()
                    if text:
                        paragraphs.append(text)
            else:
                # 如果找不到指定的文章容器，尝试获取所有段落
                for p in soup.find_all(['p', 'article', 'section']):
                    text = p.get_text().strip()
                    if text and len(text) > 10:  # 只保留较长的段落，避免无意义的短文本
                        paragraphs.append(text)

            # print('检测到的文章内容',paragraphs)
            q = Q()
            q &= Q(is_active=True)

            # 进行关键词检测
            # 获取所有已启用的关键词
            total, sensitive_words_list = await sensitive_word_controller.list(page=1, page_size=5000, search=q)

            # 将 sensitive_words_list 转换成集合
            sensitive_words = set([sensitive_word.word.lower() for sensitive_word in sensitive_words_list])

            # 2. 定位敏感词及其句子
            sensitive_sentences = []
            for paragraph in paragraphs:
                found_words_in_paragraph = [word for word in sensitive_words if word.lower() in paragraph.lower()]
                if found_words_in_paragraph:
                    sensitive_sentences.append({
                        "sentence": paragraph,
                        "found_words": found_words_in_paragraph
                    })

            # 3. 生成PDF报告并上传到OSS
            timestamp = int(time.time())
            pdf_filename = f"sensitive_report_{timestamp}.pdf"  # 使用时间戳作为唯一标识符
            self.generate_sensitive_report_pdf(sensitive_sentences, pdf_filename, crawler, title_text)

            # 上传到OSS
            object_name = f"sensitive_reports/{pdf_filename}"
            oss_url = upload_to_oss(pdf_filename, object_name)

            # 清理本地生成的PDF文件
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)
                print(f"已删除本地文件：{pdf_filename}")

            if oss_url:
                print(f"报告已上传到OSS：{oss_url}")
                # 更新crawler的result_url字段
                crawler.result_url = oss_url
                await crawler.save()
                return True  # 表示成功生成报告并上传
            else:
                print("报告生成成功，但上传到OSS失败。")
                return False  # 表示生成报告成功，但上传失败

        else:
            # 请求失败（虽然上面已经用 raise_for_status 处理了，这里作为备用）
            print(f"请求失败，状态码：{response.status_code}")
            await crawler.save()
            return False

    def generate_sensitive_report_pdf(self, sensitive_sentences, filename, crawler=None, title_text=None):
        # 注册Arial字体
        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'Arial.ttf')
        pdfmetrics.registerFont(TTFont('Arial', font_path))

        # 创建一个带有水印的画布类
        class WatermarkCanvas(canvas.Canvas):
            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self._saved_page_states = []

            def showPage(self):
                self._saved_page_states.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                # 添加水印到每一页
                for state in self._saved_page_states:
                    self.__dict__.update(state)
                    self.setFont("Arial", 30)
                    self.setFillColor(colors.lightgrey)
                    self.saveState()
                    self.translate(letter[0] / 2, letter[1] / 2)
                    self.rotate(45)
                    self.drawCentredString(0, 0, "网页敏感词检测")
                    self.restoreState()
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)

        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Story = []
        styles = getSampleStyleSheet()

        # 设置所有样式使用Arial字体
        for style in styles.byName.values():
            style.fontName = 'Arial'

        # 创建自定义样式
        sensitive_style = styles['Normal'].clone('SensitiveWord')
        sensitive_style.textColor = red
        styles.add(sensitive_style)

        Story.append(Paragraph("敏感词检测报告", styles['Heading1']))
        Story.append(Spacer(1, 12))

        # 统计敏感词出现次数
        word_count = {}
        total_count = 0
        if sensitive_sentences:
            for item in sensitive_sentences:
                sentence = item["sentence"]
                found_words = item["found_words"]
                for word in found_words:
                    # 统计每个敏感词在当前句子中的出现次数
                    count = sentence.lower().count(word.lower())
                    word_count[word] = word_count.get(word, 0) + count
                    total_count += count

            # 生成统计摘要
            summary = f"总结：共检测出{total_count}条敏感词，其中"
            word_stats = [f"‘{word}’出现{count}次" for word, count in word_count.items()]
            summary += "，".join(word_stats)

            Story.append(Paragraph(summary, styles['Normal']))
            Story.append(Spacer(1, 12))

        # 格式化当前时间
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 添加基本信息段落
        if crawler and title_text:
            # 添加爬虫任务基本信息
            Story.append(Paragraph("爬虫任务信息", styles['Heading2']))
            Story.append(Spacer(1, 12))

            basic_info = f"爬取时间：{current_time}<br/>"
            basic_info += f"目标网站：{crawler.url}<br/>"
            basic_info += f"文章标题：{title_text}<br/>"
            basic_info += f"请求方法：{crawler.method}<br/>"
            basic_info += f"请求参数：{crawler.params}<br/>"
            basic_info += f"请求头：{crawler.headers}"
        else:
            # 添加文本检测基本信息
            Story.append(Paragraph("文本检测信息", styles['Heading2']))
            Story.append(Spacer(1, 12))

            basic_info = f"检测时间：{current_time}<br/>"
            basic_info += f"检测类型：直接文本检测"

        Story.append(Paragraph(basic_info, styles['Normal']))
        Story.append(Spacer(1, 12))

        if sensitive_sentences:
            # print(sensitive_sentences)
            Story.append(Paragraph("检测结果文档标记", styles['Heading2']))
            Story.append(Spacer(1, 12))

            for item in sensitive_sentences:
                sentence = item["sentence"]
                found_words = item["found_words"]

                # 标记所有敏感词的位置
                marks = []  # 存储格式: (起始位置, 结束位置)

                for word in found_words:
                    start_pos = 0
                    while True:
                        pos = sentence.find(word, start_pos)
                        if pos == -1:
                            break
                        marks.append((pos, pos + len(word)))
                        start_pos = pos + 1  # 从下一个位置继续查找

                # 按位置排序
                marks.sort()

                # 合并重叠区间（如果有的话）
                if marks:
                    merged_marks = [marks[0]]
                    for current in marks[1:]:
                        prev = merged_marks[-1]
                        if current[0] < prev[1]:
                            merged_marks[-1] = (prev[0], max(prev[1], current[1]))
                        else:
                            merged_marks.append(current)

                    # 构建带有标记的文本
                    result_text = ""
                    last_end = 0
                    for start, end in merged_marks:
                        # 添加敏感词前的普通文本
                        result_text += sentence[last_end:start]
                        # 添加带颜色的敏感词
                        result_text += f'<font color="red">{sentence[start:end]}</font>'
                        last_end = end

                    # 添加最后剩余的文本
                    result_text += sentence[last_end:]

                    Story.append(Paragraph(result_text, styles['Normal']))
                    Story.append(Spacer(1, 6))
        else:
            Story.append(Paragraph("检测结果：未发现敏感词", styles['Heading2']))
            Story.append(Spacer(1, 12))
            Story.append(Paragraph("本次检测未发现任何敏感词。", styles['Normal']))

        # 使用带水印的画布构建文档
        doc.build(Story, canvasmaker=WatermarkCanvas)

    async def check_text_content(self, sentences: list):
        """检测文本内容中的敏感词并生成报告

        Args:
            sentences: 需要检测的文本内容列表

        Returns:
            str: 生成的报告URL，如果失败则返回None
        """
        try:
            q = Q()
            q &= Q(is_active=True)

            # 获取所有已启用的关键词
            total, sensitive_words_list = await sensitive_word_controller.list(page=1, page_size=5000, search=q)

            # 将 sensitive_words_list 转换成集合
            sensitive_words = set([sensitive_word.word.lower() for sensitive_word in sensitive_words_list])

            # 定位敏感词及其句子
            sensitive_sentences = []
            for sentence in sentences:
                found_words = [word for word in sensitive_words if word in sentence]
                if found_words:
                    sensitive_sentences.append({
                        "sentence": sentence,
                        "found_words": found_words
                    })

            # 生成PDF报告并上传到OSS
            timestamp = int(time.time())
            pdf_filename = f"sensitive_report_{timestamp}.pdf"
            self.generate_sensitive_report_pdf(sensitive_sentences, pdf_filename)

            # 上传到OSS
            object_name = f"sensitive_reports/{pdf_filename}"
            oss_url = upload_to_oss(pdf_filename, object_name)

            # 清理本地生成的PDF文件
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)
                print(f"已删除本地文件：{pdf_filename}")

            if oss_url:
                print(f"报告已上传到OSS：{oss_url}")
                return oss_url
            else:
                print("报告生成成功，但上传到OSS失败。")
                return None

        except Exception as e:
            print(f"检测文本内容时发生错误: {e}")
            return None


crawler_controller = CrawlerController()
