<template>
    <div class="read-container">
        <div class="chapter-nav">
            <div class="prev-page" @click="getPrevPage" :class="{disable: isActive.disable_prev_btn}">
                <span>Предыдущая страница</span></div>
            <div class="open" @click="show_menu = !show_menu"><span>Оглавление</span></div>
            <div class="next-page" @click="getNextPage" :class="{disable: isActive.disable_next_btn}">
                <span>Следующая страница</span>
            </div>
        </div>
        <transition name="chapterMenu">
            <div v-if="show_menu" class="chapter-menu">
                <h4>ОГЛАВЛЕНИЕ</h4>
                <div class="search-chapter">
                    <input type="text" placeholder="Найти главу" v-model="search_text" @input="searchChapter">
                </div>
                <h4>Главы</h4>
                <div class="chapter-container" v-on:scroll="scrollLoadChapters">
                    <a v-for="(chapter, index) in this.chapters" :key="chapter.id" @click="selectPage(chapter.id)">
                        <span>{{index + 1}}|{{chapter.chapter_name}}</span>
                    </a>
                </div>
            </div>
        </transition>
        <div class="chapter-content">
            <div class="chapter-name">{{selectedChapter.name}}</div>
            <div class="chapter_text" v-html="selectedChapter.text"></div>
        </div>
        <div class="chapter-nav">
            <div class="prev-page"><span>Предыдущая страница</span></div>
            <div class="open"><span>Оглавление</span></div>
            <div class="next-page">
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
                chapters: [],
                next_page_link: '',
                previous_page_link: null,
                show_menu: false,
                search_text: '',
                read_history: {
                    last_chapter: null,
                    page: null,
                },
                selectedChapter: {
                    id: null,
                    name: null,
                    text: null,
                },
                isActive: {
                    scrollLoad: true,
                    disable_next_btn: false,
                    disable_prev_btn: false,
                },
                headers: {headers: {'Authorization': "JWT " + this.$store.state.token}},
            }
        },
        methods: {
            checkBtn() {
                let selected_position = this.getPositionLoop()
                if (selected_position === 0) {
                    this.isActive.disable_prev_btn = true
                    this.isActive.disable_next_btn = false
                } else if (selected_position === this.chapters.length - 1) {
                    this.isActive.disable_next_btn = true
                    this.isActive.disable_prev_btn = false
                } else {
                    this.isActive.disable_prev_btn = false
                    this.isActive.disable_next_btn = false
                }

            },
            searchChapter() {
                let url = "http://127.0.0.1:8000/ranobe/" + this.ranobeId + "/chapters/?search=" + this.search_text;
                axios.get(url)
                    .then(resp => {
                            this.chapters = resp.data.results
                        }
                    )
            },
            scrollLoadChapters() {
                if (this.isActive.scrollLoad) {
                    let a = document.querySelector('.chapter-container').scrollTop;
                    let b = (document.querySelector('.chapter-container').scrollHeight - document.querySelector('.chapter-container').clientHeight)
                    if (Math.round(a) === b) {
                        this.loadNextPageOfChapters()
                    }
                }
            },
            getFirst() {
                let url = `http://127.0.0.1:8000/ranobe/${this.ranobeId}/chapters/`
                axios.get(url)
                    .then(resp => {
                        this.chapters = resp.data.results
                        this.next_page_link = resp.data.next
                        this.previous_page_link = resp.data.prev
                        if (this.chapters.length > 0) {
                            this.selectPage(this.chapters[0].id)
                        }
                    }).catch(er => console.log(er))
            },
            selectPage(chapter_id) {
                if (chapter_id !== null && chapter_id !== undefined) {
                    let url = `http://127.0.0.1:8000/ranobe/chapters/read/${chapter_id}/`
                    axios.get(url)
                        .then(resp => {
                            this.selectedChapter.id = resp.data.id
                            this.selectedChapter.name = resp.data.chapter_name;
                            this.selectedChapter.text = resp.data.text
                            this.show_menu = false
                            this.checkBtn()
                        }).catch(er => console.log(er))
                }
            },
            loadNextPageOfChapters: function () {
                if (this.next_page_link !== null && this.next_page_link !== undefined) {
                    axios.get(this.next_page_link).then(resp => {
                        this.next_page_link = resp.data.next;
                        this.chapters = this.chapters.concat(resp.data.results)
                    }).catch(er => console.log(er))
                }
            },
            getReadHistory() {
                if (this.$store.state.token !== null) {
                    let url = `http://127.0.0.1:8000/ranobe/${this.ranobeId}/history/`
                    axios.get(url, this.headers)
                        .then(resp => {
                            if (resp.data.res !== false) {
                                this.read_history.last_chapter = resp.data.res.ranobe_chapter
                                this.read_history.page = resp.data.page
                                this.uploadChapterData()
                            }
                        }).catch(er => {
                        console.log(er)
                    })
                }
            },
            uploadChapterData() {
                if (this.read_history.page !== null || this.read_history.page !== 1) {
                    let url = `http://127.0.0.1:8000/ranobe/${this.ranobeId}/chapters/?page_size=10000`
                    axios.get(url)
                        .then(resp => {
                            this.chapters = resp.data.results
                            this.next_page_link = resp.data.next
                            this.selectPage(this.read_history.last_chapter)
                        })
                }
            },
            getPositionLoop() {
                for (let i = 0; i < this.chapters.length; i++) {
                    if (this.chapters[i].id === this.selectedChapter.id) {
                        return i
                    }
                }
                return -1
            },
            getNextPage() {
                if (this.isActive.disable_next_btn === false) {
                    if (this.next_page_link === null || this.next_page_link === undefined) {
                        let chapter_position = this.getPositionLoop()
                         if (chapter_position !== this.chapters.length && this.chapters.length > 1 && chapter_position !== -1) {
                            this.selectPage(this.chapters[chapter_position + 1].id)
                            this.addToHistory()
                        }

                    } else {
                        let chapter_position = this.getPositionLoop()
                        if (chapter_position > this.chapters.length - 10) {
                            this.loadNextPageOfChapters()
                            this.selectPage(this.chapters[chapter_position + 1].id)
                            this.addToHistory()
                        }
                    }
                }
            },
            getPrevPage() {
                if (this.isActive.disable_prev_btn === false) {
                    let chapter_position = this.getPositionLoop()
                    if (chapter_position !== 0) {
                        this.selectPage(this.chapters[chapter_position - 1].id)
                        this.addToHistory()
                    }
                }
            },
            addToHistory() {
                if (this.$store.state.token !== null) {
                    if (this.selectedChapter.id !== null && this.selectedChapter.id !== undefined) {
                        let url = `http://127.0.0.1:8000/ranobe/${this.ranobeId}/history/`;
                        let _data = new FormData()
                        _data.append('chapter_id', this.selectedChapter.id)
                        axios.post(url, _data, this.headers).catch(er => console.log(er))
                    }
                }
            }
        },
        mounted() {
            //Fix with event saving in $window and get request
            window.removeEventListener('scroll', this.getNext_page);
            this.getFirst();
            this.getReadHistory();
        }
        ,
    }
</script>

<style scoped>

    .open {
        margin-left: 10px;
        margin-right: 10px;
    }
    .prev-page {
    }
    .prev-page.disable:hover, .next-page.disable:hover {
        background-color: rgba(255, 0, 0, 0.11);
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
    @media screen and (min-width: 130px) and (max-width: 650px) {
        .chapter-nav > div {
            font-size: 14px;
            text-align: center;
        }
        .read-container {
            padding: 0;
        }
        .chapter-nav {
            width: 100%;
            padding: 0;
            margin: 0 auto 13px;
         }

    }

</style>