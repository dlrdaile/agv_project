import request from '@/utils/request'
import store from '@/store'
export function createOrder(data) {
  return request({
    url: '/' + store.getters.roles[0] + '/order' + '/create',
    method: 'post',
    data
  })
}

export function updateOrder(data) {
  return request({
    url: '/' + store.getters.roles[0] + '/order' + '/update',
    method: 'post',
    data
  })
}

export function getOrderList(query) {
  return request({
    url: '/' + store.getters.roles[0] + '/order' + '/getlist',
    method: 'post',
    data: query
  })
}

export function deleteOrder(order_id) {
  return request({
    url: '/' + store.getters.roles[0] + '/order' + '/delete',
    method: 'delete',
    params: {
      order_id: order_id
    }
  })
}
