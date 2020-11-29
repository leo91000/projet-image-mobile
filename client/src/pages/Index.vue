<template>
  <q-page class="flex w-100">
    <img
      alt="Quasar logo"
      src="~assets/quasar-logo-full.svg"
      v-if="loading"
    >
    <div v-else class="q-pa-md row items-start q-gutter-md w-100">
      <q-card v-for="(image, i) in imageList" :key="image.id" class="image-button flex flex-center w-100 image-height" @click.stop="redirectToImageSearch(image.id)">
        <q-img :src="`${apiEndpoint}${image.url}`" basic :alt="`image${i}`" height="200" class="image-height">
          <div class="absolute-bottom text-subtitle1 text-center">
            {{ `Image ${i + 1}` }}
          </div>
        </q-img>
      </q-card>
    </div>
  </q-page>
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
      imageList: 'getImageList',
      loading: 'getLoading'
    })
  },
  created () {
    this.fetchImageList()
  },
  methods: {
    ...mapActions('images', ['fetchImageList']),
    redirectToImageSearch (imageId) {
      this.$router.push(`/image-search/${imageId}`)
    }
  }
}
</script>

<style>
.image-button {
  background-color: transparent;
  border-radius: 5px;
  transition: box-shadow 0.3s ease-in-out;
}

.image-button:hover {
  box-shadow: 0 0 10px #1D1D1D;
  cursor: pointer;
}

.w-100 {
  width: 100%;
}

.image-height {
  height: 300px!important;
}
</style>
