import request from '@/utils/request'
import store from '@/store'

export function setCarStatus(ctl_code) {
  return request({
    url: '/admin' + '/cars/setStatus',
    method: 'post',
    params: {
      car_id: 1,
      ctl_code: parseInt(ctl_code)
    }
  })
}

export function runDemoMove(taskId) {
  return request({
    url: '/admin' + '/cars/runDemo',
    method: 'post',
    params: {
      taskId: taskId,
    }
  })
}
