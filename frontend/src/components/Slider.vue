<template>
    <div>
        <div class="name-header">
            <h3>Последние обновления</h3>
        </div>
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
        <div class="name-header">
            <h3>Популярное</h3>
        </div>
        <swiper class="swiper" :options="swiperOption">
            <swiper-slide v-for="(slide, index) in slider_content_l" :key="slide.name + (index)" class="ranobe-container">
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
            getRanobes() {
                axios.get('http://127.0.0.1:8000/ranobe/')
                    .then(resp => {
                        this.slider_content = resp.data.results
                    }).catch(er => {
                    console.log(er)
                })
            },
            getRanobesWithLikes() {
                let url = 'http://127.0.0.1:8000/ranobe/?likes=1'
                axios.get(url).then(resp => {
                    this.slider_content_l = resp.data.results
                }).catch(er => console.log(er))
            },
        },
        mounted() {
            this.getRanobes();
            this.getRanobesWithLikes();
        }
    }
</script>

<style scoped>
    .name-header {
        display: inline-flex;
    }

    .name-header > h3 {
        font-size: 1.5em;
        font-weight: 400;
    }

    .name-header > h3:before {
        color: #4183c4;
        content: '#';
        padding-left: 10px;
        padding-right: 5px;
    }

    .swiper {
        height: auto;
        width: 100%;
    }

    .ranobe-container {
        width: 250px;
        height: 280px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .ranobe-image-cont {
        max-height: 100%;
        min-height: 100%;
    }

    .ranobe-img {
        object-fit: cover;
        height: 100%;
        max-height: 290px;
        width: 100%;
        border-radius: 5px;
        border: 1px solid #cecece;
    }

    .ranobe-img-adult {
        object-fit: cover;
        height: 100%;
        max-height: 290px;
        width: 100%;
        border-radius: 5px;
        filter: blur(3px);
    }

    .ranobe-header {
        background: rgba(0, 0, 0, .8);
        position: relative;
        bottom: 19.5%;
        height: 60px;
    }

    .ranobe-header span {
        margin-left: 1.5%;
        margin-right: 1.5%;
        color: #fff;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: pre;
        float: left;
        width: 97%;
        text-align: center;
    }
</style>