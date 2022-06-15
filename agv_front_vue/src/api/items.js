import request from '@/utils/request'

export function getItemList(roles, data) {
  return request({
    url: roles + '/items/getitems',
    method: 'post',
    data
  })
}

export function getItemListForSearch(roles) {
  return request({
    url: roles + '/items/getitems',
    method: 'get'
  })
}

export function deleteItem(roles, item_id) {
  return request({
    url: roles + '/items/delete',
    method: 'delete',
    params: {
      item_id: item_id
    }
  })
}

export function getItemProcess(roles, item_id) {
  return request({
    url: roles + '/items/getitemprocess',
    method: 'get',
    params: {
      item_id: item_id
    }
  })
}

export function updateItem(roles, data) {
  return request({
    url: roles + '/items/update',
    method: 'post',
    data
  })
}
