import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/oauth/token',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/oauth/logout',
    method: 'post'
  })
}
