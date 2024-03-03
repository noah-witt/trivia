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
import luxon from 'luxon'

const REFRESH_INTERVAL = luxon.Duration.fromMillis(30 * 1000)

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
      quiz: null as null | Quiz,
      leaderboardLastRefresh: luxon.DateTime.fromMillis(0),
      leaderboardRefreshInProgress: false
    }
  },
  methods: {
    updateLeaders () {
      if (this.leaderboardRefreshInProgress) {
        return
      }
      this.leaderboardRefreshInProgress = true
      fetch(`/api/quiz/${this.$route.params.quizId}/leaders`)
        .then((response) => response.json())
        .then((data: Leaderboard) => {
          this.leaderboard = data
          this.leaderboardLastRefresh = luxon.DateTime.now()
        })
        .finally(() => {
          this.leaderboardRefreshInProgress = false
        })
    },
    loadData () {
      fetch(`/api/quiz/${this.$route.params.quizId}`)
        .then((response) => response.json())
        .then((data: Quiz) => {
          this.quiz = data
        })
      this.updateLeaders()
    }
  },
  mounted () {
    this.loadData()
    setInterval(() => {
      const age = luxon.DateTime.now().diff(this.leaderboardLastRefresh)
      if (age > REFRESH_INTERVAL) {
        this.updateLeaders()
      }
    }, 1000)
  }
})
</script>
