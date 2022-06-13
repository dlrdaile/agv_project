import request from '@/utils/request'

export function getProcessList() {
  return request({
    url: '/commons/processlist',
    method: 'get'
  })
}
