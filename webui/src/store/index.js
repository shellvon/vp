import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        transition: {
            namespaced: true,
            state: {
                transitionName: '',
                action: []
            },
            mutations: {
                setTransition(state, transition)
                {
                    state.transitionName = transition;
                }
            }
        },
        movie: {
            namespaced: true,
            state: {
                currentMovie: {}
            },
            mutations: {
                setCurrentMovie(state, movie)
                {
                    state.currentMovie = movie
                }
            }
        }
    }
})