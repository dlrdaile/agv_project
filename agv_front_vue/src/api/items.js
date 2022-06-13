import request from '@/utils/request'

export function getItemList(roles, data) {
  return request({
    url: roles + '/items/getitems',
    method: 'post',
    data
  })
}

export function deleteItem(roles, item_id) {
  return request({
    url: roles + '/items/deleteitem',
    method: 'delete',
    params: {
      item_id: item_id
    }
  })
}
