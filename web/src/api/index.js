import { request } from '@/utils'

export default {
  login: (data) => request.post('/base/access_token', data, { noNeedToken: true }),
  getUserInfo: () => request.get('/base/userinfo'),
  getUserMenu: () => request.get('/base/usermenu'),
  getUserApi: () => request.get('/base/userapi'),
  // profile
  updatePassword: (data = {}) => request.post('/base/update_password', data),
  // users
  getUserList: (params = {}) => request.get('/user/list', { params }),
  getUserById: (params = {}) => request.get('/user/get', { params }),
  createUser: (data = {}) => request.post('/user/create', data),
  updateUser: (data = {}) => request.post('/user/update', data),
  deleteUser: (params = {}) => request.delete(`/user/delete`, { params }),
  resetPassword: (data = {}) => request.post(`/user/reset_password`, data),
  // role
  getRoleList: (params = {}) => request.get('/role/list', { params }),
  createRole: (data = {}) => request.post('/role/create', data),
  updateRole: (data = {}) => request.post('/role/update', data),
  deleteRole: (params = {}) => request.delete('/role/delete', { params }),
  updateRoleAuthorized: (data = {}) => request.post('/role/authorized', data),
  getRoleAuthorized: (params = {}) => request.get('/role/authorized', { params }),
  // menus
  getMenus: (params = {}) => request.get('/menu/list', { params }),
  createMenu: (data = {}) => request.post('/menu/create', data),
  updateMenu: (data = {}) => request.post('/menu/update', data),
  deleteMenu: (params = {}) => request.delete('/menu/delete', { params }),
  // apis
  getApis: (params = {}) => request.get('/api/list', { params }),
  createApi: (data = {}) => request.post('/api/create', data),
  updateApi: (data = {}) => request.post('/api/update', data),
  deleteApi: (params = {}) => request.delete('/api/delete', { params }),
  refreshApi: (data = {}) => request.post('/api/refresh', data),
  // depts
  getDepts: (params = {}) => request.get('/dept/list', { params }),
  createDept: (data = {}) => request.post('/dept/create', data),
  updateDept: (data = {}) => request.post('/dept/update', data),
  deleteDept: (params = {}) => request.delete('/dept/delete', { params }),
  // auditlog
  getAuditLogList: (params = {}) => request.get('/auditlog/list', { params }),
  // sensitive_word
  getSensitiveWordList: (params = {}) => request.get('/sen_words/list', { params }),
  createSensitiveWord: (data = {}) => request.post('/sen_words/create', data),
  updateSensitiveWord: (data = {}) => request.post('/sen_words/update', data),
  deleteSensitiveWord: (params = {}) => request.delete('/sen_words/delete', { params }),
  toggleSensitiveWord: (wordId) => request.post(`/sen_words/toggle?word_id=${wordId}`),
  // crawler
  getCrawlerList: (params = {}) => request.get('/crawler/list', { params }),
  createCrawler: (data = {}) => request.post('/crawler/create', data),
  updateCrawler: (data = {}) => request.post('/crawler/update', data),
  deleteCrawler: (params = {}) => request.delete('/crawler/delete', { params }),
  doCrawler: (data = {}) => request.post('/crawler/do_crawler', data),
  checkText: (data = {}) => request.post('/crawler/check_text', data),
  getBase64: (data = {}) => request.post('/crawler/get_base64', data),
}
