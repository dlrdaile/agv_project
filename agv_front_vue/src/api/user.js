import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/oauth/login',
    method: 'post',
    data
  })
}

export function getInfo(user_id) {
  return request({
    url: '/commons/userinfo',
    method: 'get',
    params: { user_id }
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

export function getUserListForSearch() {
  return request({
    url: '/admin/user/getuserlist',
    method: 'get'
  })
}

