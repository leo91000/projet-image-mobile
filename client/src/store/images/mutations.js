export function setImageList (state, data) {
  state.imageList = data
}

export function setLoading (state, data) {
  state.loading = !!data
}

export function setImageSearchResult (state, data) {
  state.imageSearchResult = data
}

export function setSearchResultFeedback (state, value) {
  state.imageSearchResult.feedback = value
}
