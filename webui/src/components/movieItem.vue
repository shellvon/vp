<template>
    <v-card color="cyan darken-2" class="white--text" >
       <v-layout row>
           <v-flex xs8>
               <v-card-title primary-title class="text-left" >
                   <div>
                       <div class="headline">{{movie.name}}</div>
                       <div>导演:{{movie.directors}}</div>
                       <div>主演:{{movie.actors}}</div>
                       <div>上映:{{movie.year}}</div>
                       <div>来源:{{movie.source}}</div>
                      <v-chip class="ml-0" small label color="pink" text-color="white" v-if="movie.note">{{movie.note}}</v-chip>
                      <v-chip class="ml-0" small label color="indigo" text-color="white" v-if="movie.download_link.length">可下载</v-chip>
                   </div>
               </v-card-title>
           </v-flex>
           <v-flex xs4 class="pa-1">
               <v-img
                   :src="movie.cover"
                   lazy-src="https://picsum.photos/10/6"
                   contain
                   >
                    <v-layout
                    slot="placeholder"
                    fill-height
                    align-center
                    justify-center
                    ma-0
                  >
                    <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                  </v-layout>
               </v-img>
           </v-flex>
       </v-layout>
       <v-divider ></v-divider>
       <v-card-actions classs="pa3">
           <v-rating
                :value="movie.score/2"
                readonly
                half-increments
                background-color="yellow lighten-3"
                color="yellow"
                small
                ></v-rating>
           <span slot="activator" color="red">{{movie.score}}</span>
           <v-spacer></v-spacer>
           <v-btn color="info" @click="watchMovie">查看</v-btn>
       </v-card-actions>
    </v-card>
</template>

<script>
export default {
    name: 'MovieItem',
    props: {
        movie: {
            type: Object,
            default: () => {
                return {}
            }
        }
    },
    methods: {
        watchMovie(){
            this.$uweb.trackEvent('movie', 'view', this.movie.name)
            this.$uweb.trackPageview(`/player?source=${this.movie.source}&${this.movie.id}&title=${this.movie.name}`, '/home')
            this.$router.push({name: 'player', query: {source: this.movie.source, id: this.movie.id, title: this.movie.name}})
        }
    }
}
</script>

<style>

.text-left {
    text-align: left;
}
</style>
