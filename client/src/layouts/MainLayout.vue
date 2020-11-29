<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Projet Image Mobile
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          Projet Image Mobile
        </q-item-label>
        <q-item v-for="(item, i) in links" :key="i" :to="item.link" exact>
          <q-item-section avatar>
            <q-icon :name="item.icon"></q-icon>
          </q-item-section>
          <q-item-section>
            {{ item.title }}
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: 'MainLayout',
  data () {
    return {
      leftDrawerOpen: false,
      links: [
        { title: 'Accueil', link: '/', icon: 'home' },
        { title: 'Indexer une image', link: '/add-image-to-database', icon: 'add_photo_alternate' },
        { title: 'Recherche d\'image', link: '/add-image-search', icon: 'search' }
      ]
    }
  }
}
</script>
