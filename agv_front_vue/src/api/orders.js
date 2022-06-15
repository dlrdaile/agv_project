import request from '@/utils/request'

const order_base_path = '/client/adminOrder'

export function createOrder(data) {
  return request({
    url: order_base_path + '/create',
    method: 'post',
    data
  })
}

export function updateOrder(data) {
  return request({
    url: order_base_path + '/update',
    method: 'post',
    data
  })
}

export function getOrderList(query) {
  return request({
    url: order_base_path + '/getlist',
    method: 'post',
    data: query
  })
}

export function deleteOrder(order_id) {
  return request({
    url: order_base_path + '/delete',
    method: 'delete',
    params: {
      order_id: order_id
    }
  })
}
