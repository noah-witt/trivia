<template>
  <div class="Trivia" v-if="quiz != null">
    <div>
      <h1>{{ quiz.title }}</h1>
      <div v-if="currentQuestionData">
        <h2>{{ currentQuestionData.question }}</h2>
        <div
          v-for="(answer, index) in currentQuestionData.answers"
          :key="index"
        >
          <input
            type="radio"
            :id="index + '-q'"
            :value="answer"
            v-model="currentQuestionResponse"
          />
          <label :for="index + '-q'">{{ answer }}</label>
        </div>
        <button v-if="ableToBack" @click="back">Back</button>
        <button v-if="ableToAdvance" @click="advance">Next</button>
        <div v-if="showSubmit">
          <input v-model="name" placeholder="Name" />
          <input v-model="email" placeholder="Email" />
          <button :disabled="!ableToSubmit" @click="submitQuiz">Submit</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

interface Question {
  question: string;
  answers: string[];
}

interface Quiz {
  key: string;
  title: string;
  questions: Question[];
}

export default defineComponent({
  name: 'TriviaDashboard',
  data () {
    return {
      quiz: null as null | Quiz,
      responses: [] as (number | undefined)[],
      currentQuestion: 0,
      name: '',
      email: ''
    }
  },
  components: {},
  mounted () {
    this.fetchQuiz()
  },
  methods: {
    fetchQuiz () {
      fetch(`/api/quiz/${this.$route.params.quizId}`)
        .then((response) => response.json())
        .then((data: Quiz) => {
          this.quiz = data
        })
    },
    submitQuiz () {
      fetch(`/api/quiz/${this.$route.params.quizId}/answer`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.name,
          email: this.email,
          responses: this.responses
        })
      }).then(() => {
        this.$router.push('/leaderboard/' + this.$route.params.quizId)
      })
    },
    advance () {
      if (this.ableToAdvance) {
        this.currentQuestion++
      }
    },
    back () {
      if (this.ableToBack) {
        this.currentQuestion--
      }
    }
  },
  computed: {
    ableToAdvance () {
      const length = this.quiz?.questions.length
      if (length === undefined) {
        return false
      }
      return this.currentQuestion < length - 1
    },
    ableToBack () {
      return this.currentQuestion > 0
    },
    showSubmit () {
      return (
        this.responses.length === this.quiz?.questions.length &&
        this.responses.every((response) => response !== undefined)
      )
    },
    ableToSubmit () {
      return (
        this.responses.length === this.quiz?.questions.length &&
        this.responses.every((response) => response !== undefined) &&
        this.name !== '' &&
        this.email !== '' &&
        this.email.includes('@')
      )
    },
    currentQuestionData () {
      return this.quiz?.questions?.[this.currentQuestion]
    },
    currentQuestionResponse: {
      get (): string | undefined {
        const index = this.responses?.[this.currentQuestion]
        if (index === undefined) {
          return undefined
        }
        return this.currentQuestionData?.answers[index]
      },
      set (value: string | undefined) {
        while (this.responses.length <= this.currentQuestion) {
          this.responses.push(undefined)
        }
        if (value === undefined) {
          this.responses[this.currentQuestion] = undefined
          return
        }
        this.responses[this.currentQuestion] =
          this.currentQuestionData?.answers.findIndex((v) => v === value)
      }
    }
  }
})
</script>
