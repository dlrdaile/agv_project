import request from '@/utils/request'

export function getEmailCode(email, path) {
  return request({
    url: '/oauth/getcode/' + path,
    method: 'get',
    params: { email }
  })
}
