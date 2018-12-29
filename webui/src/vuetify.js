import Vue from 'vue';
import {
    Vuetify,
    VApp,
    VBtn,
    VCard,
    VDivider,
    VGrid,
    VIcon,
    VList,
    VChip,
    VProgressLinear,
    VTextField,
    VImg,
    VAvatar,
    VSelect,
    VAutocomplete,
    VRating,
    VSnackbar,
    VDialog,

} from 'vuetify'

import {
    VRadio,
    VRadioGroup,
    VExpansionPanel,
    VSlideYTransition,
    VExpansionPanelContent,
    VProgressCircular,
}
from 'vuetify/lib'

import 'vuetify/src/stylus/app.styl'

Vue.use(Vuetify, {
    components: {
        VApp,
        VBtn,
        VCard,
        VDivider,
        VGrid,
        VIcon,
        VList,
        VChip,
        VProgressLinear,
        VTextField,
        VImg,
        VAvatar,
        VSlideYTransition,
        VSelect,
        VAutocomplete,
        VRating,
        VSnackbar,
        VExpansionPanel,
        VExpansionPanelContent,
        VProgressCircular,
        VDialog,
        VRadioGroup,
        VRadio,
    },
    theme: {
        primary: '#4DBA87'
    }
})