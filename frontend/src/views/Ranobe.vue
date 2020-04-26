<template>
    <div id="ranobe-page">
        <div class="left-to-top">
            <div class="sticky-go-top" @click="goTop" v-if="!last_window_position">
            </div>
            <div class="sticky-go-back" @click="goTop" v-else></div>
        </div>
        <div class="content-hover-container">
            <div class="search">
                <form>
                    <input class="search-input" type="text" placeholder="Введите название Ранобэ" v-model="search_text">
                    <button id="clear-b" class="search-button" @click="searchClear">Очистить</button>
                    <button id="search-b" class="search-button" @click="search">Поиск</button>

                </form>
            </div>
            <transition name="ranobe-trans">
                <div class="content">
                    <div class="ranobe-container" v-for="(ranobe, index) in ranobes" :key="`item-${index}`">
                        <div class="ranobe-image-cont">
                            <router-link class="ran-link"
                                         :to="{ name: 'RanobeDetail', params: { ranobeId: ranobe.id }}">
                                <img class="ranobe-img" v-bind:src="ranobe.image" alt=""
                                     v-if="ranobe.adult_status === false">
                                <img class="ranobe-img-adult" v-bind:src="ranobe.image" alt="" v-else>
                            </router-link>
                            <div class="ranobe-header">
                                <span class="ranobe-name">{{normalizeRanobeName(ranobe.name)}}</span><span
                                    class="ranobe-alternate-n"
                                    v-if="ranobe.alternate_name">{{ranobe.alternate_name}}</span>
                                <span class="ranobe-alternate-n" v-else> </span>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
        <Menu @update="sync" @clear="getFirst" @disable="searchActiveDisable"
              v-bind:_filter="{tag: choosed_tag, genre: choosed_genre}"></Menu>
    </div>
</template>
<style scoped>

    .left-to-top {
        position: absolute;
        height: 0;
        width: 0;
        top: 60px;
    }
    .sticky-go-top {
        transition: all ease .5s;
        position: fixed;
        top: 50px;
        left: 0;
        width: 3%;
        height: 100%;
    }
    .sticky-go-top:hover {
        background: url('http://127.0.0.1:8080/up.svg') no-repeat center #d5d5d5;
    }
    .sticky-go-back {
        transition: all ease .5s;
        position: fixed;
        top: 50px;
        left: 0;
        width: 3%;
        height: 100%;
    }
    .sticky-go-back:hover {
        background: url('http://127.0.0.1:8080/down.svg') no-repeat center #d5d5d5;
    }
    #ranobe-page {
        display: flex;
        flex-direction: row;
    }
    .content-hover-container {
        width: 80%;
    }
    .search {
        width: 80%;
        margin: 15px auto;
    }
    .ran-link {
        clear: both;
    }
    .search > form {
        width: 100%;
        height: 34px;
        display: inline-flex;
    }
    #clear-b {
        background-color: white;
        width: 15%;
    }
    .search-input {
        border: 1px solid #acadad;
        padding-left: 15px;
        background: #fff;
        font-weight: 300;
        font-style: italic;
        font-size: 14px;
        transition: .3s;
        height: 100%;
        width: 100%;
    }
    .search-button {
        border: 1px solid #acadad;
        height: 111%;
        width: 30%;
    }
    .search-button:hover {
        transition: 0.3s ease;
    }
    .content {
        padding: 7px 7px;
        border-radius: 5px;
        background-color: #fff;
        margin-top: 25px;
        display: grid;
        grid-template-rows: auto;
        margin-left: 4%;
        width: 94%;
        grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
        grid-column-gap: 10px;
        grid-row-gap: 15px;
        box-shadow: 0 0 1px 1px rgba(0, 0, 0, 0.1);
    }
    .ranobe-image-cont {
        max-height: 100%;
        min-height: 100%;
    }
    .ranobe-container:hover {
        transition: 0.3s ease;
        -webkit-transform: scale(1.05);
        -ms-transform: scale(1.05);
        transform: scale(1.05);
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
    .ranobe-container {
        min-width: 97%;
        height: 280px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
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
    /*.ranobe-refresh*/
    @media screen and (min-width: 130px) and (max-width: 650px) {
        .content-hover-container {
            width: 100%;
        }
        .search > form {
            width: 100%;
            margin-left: auto;
            margin-right: auto;
        }
        .content {
            padding-left: 0;
            padding-right: 0;
            margin-left: 0;
            width: 100%;
            grid-template-columns: 1fr 1fr;
        }
        .search {
            width: 100%;
            margin-left: auto;
            margin-right: auto;
        }
        .search > form > input {
            width: 60%;
        }
        #clear-b {
            width: 20%;
        }
        #search-b {
            width: 20%;
        }
    }
    @media screen and (max-width: 1000px) and (min-width: 651px) and (min-height: 350px) and (max-height: 600px){
        
    }

</style>
<script>
    import axios from 'axios'
    import Menu from "../components/Menu";

    export default {
        name: "Ranobe",
        components: {Menu},
        props: ['choosedTag', 'choosedGenre'],
        data() {
            return {
                ranobes: [],
                next_page_link: null,
                search_text: '',
                last_window_position: null,
                search_active: false,
                choosed_tag: this.choosedTag,
                choosed_genre: this.choosedGenre,
            }
        },
        methods: {
            searchClear() {
                this.ranobes = []
                this.search_text = ''
                this.search_active = false
                this.getFirst()

            },
            getFirst() {
                if (this.search_active !== true) {
                    axios.get('http://127.0.0.1:8000/ranobe/')
                        .then(resp => {
                            this.next_page_link = resp.data.next;
                            for (let i = 0; i < resp.data.results.length; i++) {
                                this.ranobes.push(resp.data.results[i])
                            }
                        }).catch(er => console.log(er));
                }
            },
            searchActiveDisable() {
                this.ranobes = [];
                this.search_active = false;
                this.getFirst()
            },
            search() {
                this.ranobes = [];
                let search_url = 'http://127.0.0.1:8000/ranobe/?search=' + this.search_text;
                axios.get(search_url)
                    .then(resp => {
                        for (let i = 0; i < resp.data.results.length; i++) {
                            this.ranobes.push(resp.data.results[i])
                        }
                        this.search_active = this.search_text.length > 0;
                    }).catch(er => console.log(er));
            },
            getNext_page() {
                if (this.search_active !== true) {
                    if (this.search_text.length === 0) {
                        if (this.next_page_link !== null) {
                            let pos1 = document.documentElement.offsetHeight;
                            let pos2 = document.documentElement.scrollTop + window.innerHeight;
                            if (pos1 === Math.floor(pos2)) {
                                axios.get(this.next_page_link)
                                    .then(resp => {
                                        this.next_page_link = resp.data.next;
                                        for (let i = 0; i < resp.data.results.length; i++) {
                                            this.ranobes.push(resp.data.results[i])
                                        }
                                    }).catch(er => console.log(er))
                            }
                        }
                    }
                }
            },
            lazyloadcontent() {
                window.addEventListener('scroll', this.getNext_page)
            },
            sync: function (args) {
                this.ranobes = args
                this.search_active = true
            },
            goTop() {
                if (this.last_window_position === null) {
                    this.last_window_position = window.scrollY;
                    window.scrollTo({
                        top: 0,
                        left: 0,
                        behavior: 'smooth'
                    })
                } else {
                    window.scrollTo({
                        top: this.last_window_position,
                        left: 0,
                        behavior: 'smooth'
                    })
                    this.last_window_position = null;
                }
            },
            normalizeRanobeName(name) {
                //  If name contains char "/" return sliced name else return full name
                if (name.indexOf('/') === -1) {
                    return name
                } else {
                    return name.substring(name.indexOf('/') + 1)
                }
            },
        },

        mounted() {
            if (this.choosedFilter !== undefined || this.choosedTag !== undefined) {
                /**/

            } else {
                this.getFirst();
                this.lazyloadcontent()
            }
        },
        created() {
        },
        destroyed() {
            window.removeEventListener('scroll', this.getNext_page)
        }

    }


</script>

