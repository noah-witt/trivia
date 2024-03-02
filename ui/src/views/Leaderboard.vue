<template>
    <div class="Trivia" v-if="leaderboard != null && quiz != null">
        <h1>{{ quiz.title }} Leaderboard</h1>
        <ol>
            <li v-for="(item, index) in leaderboard" :key="index">
                {{ item.name }}: {{ item.score }}
            </li>
        </ol>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </template>

<script lang="ts">
import { defineComponent } from 'vue'

interface Quiz {
    title: string;
}

interface LeaderboardItem {
    name: string;
    score: number;
}
type Leaderboard = LeaderboardItem[];

export default defineComponent({
  name: 'LeaderboardQuiz',
  data () {
    return {
      leaderboard: null as null | Leaderboard,
      quiz: null as null | Quiz
    }
  },
  methods: {
    loadData () {
      fetch(`/api/quiz/${this.$route.params.quizId}`)
        .then((response) => response.json())
        .then((data: Quiz) => {
          this.quiz = data
        })
      fetch(`/api/quiz/${this.$route.params.quizId}/leaders`).then((response) => response.json()).then((data: Leaderboard) => {
        this.leaderboard = data
      })
    }
  },
  mounted () {
    this.loadData()
  }
})
</script>
