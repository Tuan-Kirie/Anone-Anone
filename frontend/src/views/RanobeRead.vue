<template>
    <div class="read-container">
        <div class="chapter-nav">
            <div class="prev-page" @click="getPreviousChapter"><span>Предыдущая страница</span></div>
            <div class="open" @click="show_menu = !show_menu"><span>Оглавление</span></div>
            <div class="next-page" @click="selectNextChapter">
                <span>Следующая страница</span>
            </div>
        </div>
        <transition name="chapterMenu">
            <div v-if="show_menu" class="chapter-menu">
                <h4>ОГЛАВЛЕНИЕ</h4>
                <div class="search-chapter">
                    <input type="text" placeholder="Найти главу" v-model="search_text" @change="searchChapter">
                </div>
                <h4>Главы</h4>
                <div class="chapter-container" v-on:scroll="lazyloadChapters">
                    <a v-for="(chapter, index) in this.chapters" :key="chapter.id">
                        <span @click="selectChapter(chapter.id, index)">{{index + 1}}|{{chapter.chapter_name}}</span>
                    </a>
                </div>
            </div>
        </transition>
        <div class="chapter-content">
            <div class="chapter-name">{{chapter_name}}</div>
            <div class="chapter_text" v-html="chapter_text"></div>
        </div>
        <div class="chapter-nav">
            <div class="prev-page" @click="getPreviousChapter"><span>Предыдущая страница</span></div>
            <div class="open" @click="show_menu = !show_menu"><span>Оглавление</span></div>
            <div class="next-page" @click="selectNextChapter">
                <span>Следующая страница</span>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from "axios";

    export default {
        name: "RanobeRead",
        props: ['ranobeId'],
        data() {
            return {
                chapter_page: '',
                show_menu: false,
                chapters: [],
                search_text: '',
                serched_chapters: [],
                ranobe_id: this.ranobeId,
                next_chapter_page: '',
                chapter_name: '',
                chapter_text: '',
                current_id: null,
                index: 0,
            }
        },
        methods: {
            searchChapter() {
                if (this.search_text.length > 0) {
                    let search_url = "http://127.0.0.1:8000/ranobe/" + this.ranobe_id + "/chapters/?search=" + this.search_text;
                    axios.get(search_url)
                        .then(
                            resp => {
                                this.chapters = resp.data.results
                            }
                        )
                }
            },
            selectChapter(id, index) {
                let url = 'http://127.0.0.1:8000/ranobe/chapters/read/' + id;
                axios.get(url)
                    .then(chapter_resp => {
                        this.chapter_text = chapter_resp.data.text;
                        this.chapter_name = chapter_resp.data.chapter_name;
                        this.current_id = chapter_resp.data.id;
                        this.index = index
                    }).catch(er => console.log(er));
            },
            checkChapterPos() {
                if (this.index < (this.chapters.length - 12) && this.next_chapter_page !== null) {
                    return true
                } else if (this.index === (this.chapters.length - 1) && this.next_chapter_page === null) {
                    return false
                } else if ((this.index >= (this.chapters.length - 12)) && this.next_chapter_page !== null) {
                    this.getNextChapterPage();
                    return true
                } else {
                    return false
                }
            },
            selectNextChapter() {
                if (this.checkChapterPos()) {
                    // console.log(this.chapters)
                    let url = 'http://127.0.0.1:8000/ranobe/chapters/read/' + (this.chapters[this.index].id + 1) + '/';
                    axios.get(url)
                        .then(chapter_resp => {
                            this.chapter_text = chapter_resp.data.text;
                            this.chapter_name = chapter_resp.data.chapter_name;
                            this.current_id = chapter_resp.data.id;
                            this.index++;
                        }).catch(er => console.log(er));
                }
            },
            getChaptersFisrt() {
                let chapter_url = 'http://127.0.0.1:8000/ranobe/' + this.ranobe_id + /chapters/;
                axios.get(chapter_url)
                    .then(resp => {
                        if (resp.data.next != null) {
                            this.next_chapter_page = resp.data.next
                        }
                        if (resp.data.results != null) {
                            let url = 'http://127.0.0.1:8000/ranobe/chapters/read/' + resp.data.results[0].id;
                            axios.get(url)
                                .then(chapter_resp => {
                                    this.chapter_text = chapter_resp.data.text;
                                    this.chapter_name = chapter_resp.data.chapter_name;
                                    this.current_id = chapter_resp.data.id
                                }).catch(er => console.log(er));
                            if (resp.data.results.length > 0) {
                                for (let i = 0; i !== resp.data.results.length; i++) {
                                    this.chapters.push(resp.data.results[i])
                                }
                            }
                        }
                    }).catch(er => console.log(er))
            },
            getNextChapterPage: function () {
                if (this.next_chapter_page != null) {
                    if (this.next_chapter_page.length > 0) {
                        axios.get(this.next_chapter_page)
                            .then(resp => {
                                this.next_chapter_page = resp.data.next;
                                if (resp.data.results != null) {
                                    if (resp.data.results.length > 0) {
                                        for (let i = 0; i !== resp.data.results.length; i++) {
                                            this.chapters.push(resp.data.results[i])
                                        }
                                    }
                                }
                            }).catch(er => console.log(er))
                    }
                }
            },
            getPreviousChapter() {
                if (this.index !== 0) {
                    // console.log(this.chapters)
                    let url = 'http://127.0.0.1:8000/ranobe/chapters/read/' + (this.chapters[this.index].id - 1) + '/';
                    axios.get(url)
                        .then(chapter_resp => {
                            this.chapter_text = chapter_resp.data.text;
                            this.chapter_name = chapter_resp.data.chapter_name;
                            this.current_id = chapter_resp.data.id;
                            this.index--;
                        }).catch(er => console.log(er));
                }
            },
            lazyloadChapters() {
                let a = document.querySelector('.chapter-container').scrollTop;
                let b = (document.querySelector('.chapter-container').scrollHeight - document.querySelector('.chapter-container').clientHeight)
                if (Math.round(a) === b) {
                    this.getNextChapterPage()
                }
            }
        },
        mounted() {
            //Fix with event saving in $window and get request
            window.removeEventListener('scroll', this.getNext_page);

            this.getChaptersFisrt();
        },
        destroyed() {

        }
    }
</script>

<style scoped>
    .open {
        margin-left: 10px;
        margin-right: 10px;
    }

    .prev-page {
    }

    .read-container {
        padding: 1em;
        width: 95%;
        margin-right: auto;
        margin-left: auto;
        margin-top: 15px;
    }

    .chapter-nav {
        display: flex;
        margin-bottom: 15px;
        background: #FFFFFF;
        height: 35px;
        align-items: center;
        padding: 5px;
    }

    .chapter-nav > div {
        cursor: pointer;
        padding: 5px;
        height: 100%;
        display: flex;
        align-items: center;

    }

    .chapter-nav > div:hover {
        border-radius: 5px;
        background-color: #b9b9b9;
    }

    .chapter-content {
        margin-bottom: 15px;
        padding: 1em;
        background: #FFFFFF;
    }

    .chapter-name {

    }

    .chapter-nav {
        display: inline-flex;
        width: 100%;
        justify-content: center;

    }

    .open {
        padding-left: 10px;
        padding-right: 10px;
    }

    .chapterMenu-enter-active, .chapterMenu-leave-active {
        transition: opacity .5s;
    }

    .chapterMenu-enter, .chapterMenu-leave-to {
        opacity: 0;
    }

    .chapter-menu {
        position: fixed;
        left: 0;
        top: 0;
        background-color: #FFFFFF;
        height: 100%;
        padding: 10px 20px;
        z-index: 9000;
        display: block;
        width: 300px;
        overflow: scroll;
    }
    .chapter-menu > h4 {
        width: 100%;
        text-align: center;
        border-bottom: 1px solid #3c3c3c;
        padding-bottom: 4px;
    }

    .chapter-container {
        height: 100%;
        overflow: auto;
        display: flex;
        flex-direction: column;
    }
    .search-chapter {
        min-width: 100%;
        padding-bottom: 10px;
        border-bottom: 1px solid #3c3c3c;
    }
    .search-chapter > input {
        min-width: 95%;
        height: 30px;
        padding-left: 6px;
    }
    .chapter-container > a {
        min-width: 100%;
        min-height: 30px;
        padding-left: 3px;
    }
    .chapter-container > a:hover {
        color: #4183c4;
        cursor: pointer;
    }
    .chapter-container > a > span {
        text-overflow: ellipsis;
        display: block;
        width: 280px;
        overflow: hidden;
        white-space: nowrap;
    }
    /*::-webkit-scrollbar {*/
    /*    -webkit-appearance: none;*/
    /*    width: 10px;*/
    /*    height: 10px;*/
    /*}*/
    /*::-webkit-scrollbar-thumb {*/
    /*    cursor: pointer;*/
    /*    border-radius: 5px;*/
    /*    background: rgba(0, 0, 0, .25);*/
    /*    transition: color .2s ease;*/
    /*}*/
    /*::-webkit-scrollbar-track {*/
    /*    background: rgba(0, 0, 0, .1);*/
    /*    border-radius: 0;*/
    /*}*/
    /*::selection {*/
    /*    background-color: #cce2ff;*/
    /*    color: rgba(0, 0, 0, .87);*/
    /*}*/
</style>