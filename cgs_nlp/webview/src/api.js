export const BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

export const api = {
  spider: BASE_URL + '/spiderapi/',
  tweets: BASE_URL + '/tweetsapi/',
  wordcloud: BASE_URL + '/wordcloudapi/',
  comment: BASE_URL + '/getcomment/',
  scrapyd: BASE_URL + '/scrapydapi/',
  lasted: BASE_URL + '/getlasted/',
  group: BASE_URL + '/getgroup/',
  weibo: BASE_URL + '/getweibo/',
  snownlp: BASE_URL + '/snownlpapi/',
  quick: BASE_URL + '/getlasted/',
  auth: {
    register: BASE_URL + '/api/auth/register/',
    login: BASE_URL + '/api/auth/login/',
    logout: BASE_URL + '/api/auth/logout/',
    current: BASE_URL + '/api/auth/current/'
  },
  history: {
    add: BASE_URL + '/api/history/add/',
    list: BASE_URL + '/api/history/list/'
  },
  export: {
    tweets: BASE_URL + '/api/export/tweets/',
    user: BASE_URL + '/api/export/user/'
  },
  hot: BASE_URL + '/api/hot/',
  compare: BASE_URL + '/api/model/compare/'
}
