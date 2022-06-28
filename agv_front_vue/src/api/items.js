import request from '@/utils/request'
import store from '@/store'
const roles = store.getters.roles[0]

export function getItemList(data) {
  return request({
    url: roles + '/items/getitems',
    method: 'post',
    data
  })
}

export function getItemListForSearch() {
  return request({
    url: roles + '/items/getitems',
    method: 'get'
  })
}

export function deleteItem(item_id) {
  return request({
    url: roles + '/items/delete',
    method: 'delete',
    params: {
      item_id: item_id
    }
  })
}

export function getItemProcess(item_id) {
  return request({
    url: roles + '/items/getitemprocess',
    method: 'get',
    params: {
      item_id: item_id
    }
  })
}

export function updateItem(data) {
  return request({
    url: roles + '/items/update',
    method: 'post',
    data
  })
}
