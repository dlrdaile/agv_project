import request from '@/utils/request'

export function getEmailCode(email) {
  return request({
    url: '/api/auth/getEmailCode?email=' + email,
    method: 'post'
  })
}

export function register(data) {
  return request({
    url: '/oauth/register',
    method: 'post',
    data
  })
}
