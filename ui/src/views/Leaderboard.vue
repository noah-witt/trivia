<template>
  <div class="Trivia" v-if="leaderboard != null && quiz != null">
    <h1>{{ quiz.title }} Leaderboard</h1>
    <DataTable :value="leaderboard" tableStyle="min-width: 50rem">
      <Column field="name" header="Name"></Column>
      <Column field="score" header="Score"></Column>
    </DataTable>
    <p>
      Last updated: {{ lastUpdated }}.
    </p>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script lang="ts">
import { DateTime } from 'luxon'
import { defineComponent } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import now from '../mixins/now'

const REFRESH_INTERVAL_MS = 30 * 1000

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
  mixins: [now],
  data () {
    return {
      leaderboard: null as null | Leaderboard,
      quiz: null as null | Quiz,
      leaderboardLastRefresh: DateTime.fromMillis(0),
      leaderboardRefreshInProgress: false,
      $updateCheck: null as null | number
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
          this.leaderboardLastRefresh = DateTime.now()
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
    this.$updateCheck = setInterval(() => {
      const age = DateTime.now().valueOf() - this.leaderboardLastRefresh.valueOf()
      if (age > REFRESH_INTERVAL_MS) {
        this.updateLeaders()
      }
    }, 1000)
  },
  beforeUnmount () {
    if (this.$updateCheck != null) {
      clearInterval(this.$updateCheck)
    }
  },
  components: {
    DataTable,
    Column
  },
  computed: {
    lastUpdated () {
      // eslint-disable-next-line no-unused-expressions
      this.now // to trigger the mixin's update
      return this.leaderboardLastRefresh.toRelative()
    }
  }
})
</script>
