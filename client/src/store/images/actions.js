import apiClient from 'boot/axios'

export async function fetchImageList ({ commit }) {
  commit('setLoading', true)
  try {
    const { data } = await apiClient.get('/img_searches')
    commit('setImageList', data)
  } catch (e) {
    console.error(e.message, e)
  } finally {
    commit('setLoading', false)
  }
}

export async function imageSearch ({ dispatch, commit }, { file, index, filename }) {
  const formData = new FormData()
  formData.append('file', file, filename)
  formData.append('index', index ? '1' : '0')

  commit('setLoading', true)
  try {
    const { data } = await apiClient.post('/img_searches', formData)
    await dispatch('getSearchResults', data.id)
    return data.id
  } catch (e) {
    console.error(e.message, e)
  } finally {
    commit('setLoading', false)
  }
}

export async function getSearchResults ({ commit }, id) {
  if (id) {
    const { data } = await apiClient.get(`/img_searches/${id}`)
    commit('setImageSearchResult', data)
    return data
  }
  return {}
}

export async function setFeedback ({ commit, getters }, { id, value }) {
  try {
    if (getters.getImageSearchResult.id === id) {
      commit('setSearchResultFeedback', value)
    }
    return await apiClient.post(`/feedback/${id}`, {
      relevance: value
    })
  } catch (e) {
    console.error(e.message, e)
  }
}
