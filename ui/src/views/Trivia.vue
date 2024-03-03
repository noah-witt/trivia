<template>
  <Card class="Trivia" v-if="quiz != null">
    <template #title>{{ quiz.title }}</template>
    <template #content>
      <div v-if="currentQuestionData">
        <h2>{{ currentQuestionData.question }} <small>({{ currentQuestion+1 }}/{{quiz.questions.length}})</small></h2>
        <div
          v-for="(answer, index) in currentQuestionData.answers"
          :key="index"
        >
          <RadioButton
            :id="index + '-q'"
            :value="answer"
            v-model="currentQuestionResponse"
          />
          <label :for="index + '-q'">{{ answer }}</label>
        </div>
        <br/>
        <Button :disabled="!ableToBack" @click="back">Back</Button> &nbsp;&nbsp;
        <Button :disabled="!ableToAdvance" @click="advance">Next</Button>
        <br/>
        <br/>
        <div v-if="showSubmit">
          <InputText v-model="name" placeholder="Name" />
          <InputText v-model="email" placeholder="Email" />
          <br/>
          <br/>
          <Button :disabled="!ableToSubmit" @click="submitQuiz">Submit</Button>
        </div>
      </div>
    </template>
  </Card>
  <Card v-else>
    <template #content>
      <p>Loading...</p>
    </template>
  </Card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Button from 'primevue/button'
import RadioButton from 'primevue/radiobutton'
import InputText from 'primevue/inputtext'
import Card from 'primevue/card'

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
  components: {
    Button,
    RadioButton,
    InputText,
    Card
  },
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
