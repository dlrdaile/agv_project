import request from '@/utils/request'

export function getMapList() {
  return request({
    url: '/commons/maplist',
    method: 'get'
  })
}
