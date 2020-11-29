<template>
  <q-page class="flex flex-center">
    <q-btn round color="primary" icon="search" size="lg" @click="captureImage" :loading="loading"></q-btn>
  </q-page>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  data: () => ({
    loading: false
  }),
  methods: {
    ...mapActions('images', ['imageSearch']),
    captureImage () {
      this.loading = true
      navigator.camera.getPicture(
        imageUri => {
          window.resolveLocalFileSystemURL(
            imageUri,
            (entry) => {
              entry.file(file => {
                this.readFile(file)
              })
            },
            (e) => {
              this.$q.notify(e.message)
            }
          )
        },
        () => {
          this.$q.notify('Could not access device camera')
        }
      )
    },
    readFile (file) {
      const reader = new FileReader()
      reader.onloadend = async () => {
        try {
          const imgBlob = new Blob([reader.result], {
            type: file.type
          })
          const id = await this.imageSearch({ file: imgBlob, filename: file.name, index: false })
          await this.$router.push(`/image-search/${id}`)
        } catch (e) {
          this.$q.notify(e.message)
        } finally {
          this.loading = false
        }
      }
      reader.readAsArrayBuffer(file)
    }
  }
}
</script>
