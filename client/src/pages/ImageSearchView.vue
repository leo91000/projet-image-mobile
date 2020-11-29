<template>
  <div class="w-100 q-pa-lg">
    <div v-if="!loading">
      <h4 class="text-center">Résultats de la recherche :
        <strong class="text-primary">
          {{ searchResult.results ? searchResult.results.length : 0 }}
        </strong>
      </h4>
      <div class="flex flex-center">
        <img
          v-if="searchResult.url"
          :alt="`Search image`"
          :src="`${apiEndpoint}${searchResult.url}`"
          class="image-height"
          height="200"
        />
      </div>
      <hr class="q-my-lg">
      <div class="flex flex-column">
        <div
          v-for="(res, i) in searchResult.results"
          :key="i"
          class="flex flex-row justify-around flex-center w-100 q-my-sm"
        >
          <img
            :alt="`Search image`"
            :src="`${apiEndpoint}${res.url}`"
            class="image-height"
            height="200"
          />
          <div class="text-h5 text-secondary">
            {{ roundNumber(res.score * 100) }} %
          </div>
        </div>
      </div>
      <div class="w-100 flex flex-center">
        <q-rating
          v-model="feedbackModel"
          size="2em"
          :max="5"
          color="primary"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { apiEndpoint } from 'boot/axios'

export default {
  data () {
    return {
      apiEndpoint
    }
  },
  computed: {
    ...mapGetters('images', {
      searchResult: 'getImageSearchResult',
      loading: 'getLoading'
    }),
    imageId () {
      return this.$route.params.id
    },
    feedbackModel: {
      get () {
        return this.searchResult.feedback ? this.searchResult.feedback : 0
      },
      set (val) {
        this.setFeedback({ id: this.searchResult.id, value: val })
      }
    }
  },
  created () {
    this.fetchResults()
  },
  watch: {
    imageId () {
      this.fetchResults()
    }
  },
  methods: {
    ...mapActions('images', ['getSearchResults', 'setFeedback']),
    fetchResults () {
      this.getSearchResults(this.imageId)
    },
    roundNumber (number) {
      return Number((number).toFixed(2))
    }
  }
}
</script>

<style>
.flex-basis-0 {
  flex-basis: 0;
}
</style>
