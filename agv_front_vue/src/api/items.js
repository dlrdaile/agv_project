import request from '@/utils/request'
import store from '@/store'

export function getItemList(data) {
  return request({
    url: store.getters.roles[0] + '/items/getitems',
    method: 'post',
    data
  })
}

export function getItemListForSearch() {
  return request({
    url: store.getters.roles[0] + '/items/getitems',
    method: 'get'
  })
}

export function deleteItem(item_id) {
  return request({
    url: store.getters.roles[0] + '/items/delete',
    method: 'delete',
    params: {
      item_id: item_id
    }
  })
}

export function getItemProcess(item_id) {
  return request({
    url: store.getters.roles[0] + '/items/getitemprocess',
    method: 'get',
    params: {
      item_id: item_id
    }
  })
}

export function updateItem(data) {
  return request({
    url: store.getters.roles[0] + '/items/update',
    method: 'post',
    data
  })
}
