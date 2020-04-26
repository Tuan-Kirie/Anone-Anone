<template>
    <div>
        <swiper class="swiper" :options="swiperOption">
            <swiper-slide v-for="slide in slider_content" :key="slide.id" class="ranobe-container">
                <div class="ranobe-image-cont">
                    <router-link class="ran-link"
                                 :to="{ name: 'RanobeDetail', params: { ranobeId: slide.id }}">
                        <img class="ranobe-img" v-bind:src="slide.image" alt=""
                             v-if="slide.adult_status === false">
                        <img class="ranobe-img-adult" v-bind:src="slide.image" alt="" v-else>
                    </router-link>
                    <div class="ranobe-header">
                        <span class="ranobe-name">{{slide.name}}</span>
                        <span class="ranobe-alternate-n"
                              v-if="slide.alternate_name">{{slide.alternate_name}}</span>
                        <span class="ranobe-alternate-n" v-else> </span>
                    </div>
                </div>
            </swiper-slide>
        </swiper>
    </div>
</template>

<script>
    import {Swiper, SwiperSlide, directive} from 'vue-awesome-swiper'
    import 'swiper/css/swiper.css'
    import axios from 'axios'

    export default {
        name: "Slider",
        props: {
            filterUrl: String
        },
        components: {
            Swiper,
            SwiperSlide
        },
        directives: {
            swiper: directive
        },
        data() {
            return {
                slider_content: [],
                slider_content_l: [],
                swiperOption: {
                    slidesPerView: document.documentElement.clientWidth  > 600 ? 6: 2,
                    slidesPerGroup: document.documentElement.clientWidth  > 600 ? 6: 2,
                    spaceBetween: 30,
                    // centeredSlides: true,
                    autoplay: {
                        delay: 4700,
                        disableOnInteraction: false

                    }
                }
            }
        },
        methods: {
            getRanobes(url) {
                axios.get(url)
                    .then(resp => {
                        if (resp.data.results !== undefined) {
                            this.slider_content = resp.data.results
                        } else {this.slider_content = resp.data}
                    }).catch(er => {
                    console.log(er)
                })
            },
        },
        mounted() {
            this.getRanobes(this.filterUrl);
        }
    }
</script>
<style scoped lang="sass">
    @import "./styles/SliderC.sass"
</style>