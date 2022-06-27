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
    url: '/commons/userinfo',
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

export function register(data) {
  return request({
    url: '/oauth/register',
    method: 'post',
    data
  })
}

export function forget(data) {
  return request({
    url: '/oauth/forget',
    method: 'post',
    data
  })
}



