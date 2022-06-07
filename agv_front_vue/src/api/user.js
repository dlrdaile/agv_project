import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/oauth/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/userinfo',
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
