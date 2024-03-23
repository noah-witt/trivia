<template>
  <Card class="Trivia bodoni-moda" v-if="quiz != null">
    <template #title>{{ quiz.title }}</template>
    <template #content>
      <Steps :model="stepItems" v-model:activeStep="currentQuestion" />
      <div v-if="currentQuestionData">
        <h2>{{ currentQuestionData.question }}</h2>
        <span class="selectorList">
        <div
          v-for="(answer, index) in currentQuestionData.answers"
          :key="index"
          class="selectors flex align-items-center"
        >
          <RadioButton
            :id="index + '-q'"
            :value="answer"
            v-model="currentQuestionResponse"
            :inputId="index+'-q'"
          />
          <label :for="index + '-q'">{{ answer }}</label>
        </div>
      </span>
        <br/>
        <Button :disabled="!ableToBack" @click="back">Back</Button> &nbsp;&nbsp;
        <Button :disabled="!ableToAdvance" @click="advance">Next</Button>
        <br/>
        <br/>
        <div v-if="showSubmit">
          <InputText v-model="name" placeholder="Name" />
          <InputText v-model="email" placeholder="Email" v-show="EMAIL_ENABLED"/>
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
import Steps from 'primevue/steps'

const EMAIL_ENABLED = process.env.VUE_APP_EMAIL_ENABLED === 'true'

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
      email: '',
      EMAIL_ENABLED: EMAIL_ENABLED
    }
  },
  components: {
    Button,
    RadioButton,
    InputText,
    Card,
    Steps
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
          email: EMAIL_ENABLED ? this.email : undefined,
          responses: this.responses
        })
      }).then(async (response) => {
        const data: {id: string; score: number} = await response.json()
        this.$router.push('/leaderboard/' + this.$route.params.quizId + '/' + data.id)
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
    stepItems (): { label: string }[] {
      return this.quiz?.questions.map((_, index) => ({
        label: ((index + 1)).toString()
      })) ?? []
    },
    ableToAdvance ():boolean {
      const length = this.quiz?.questions.length
      if (length === undefined) {
        return false
      }
      return this.currentQuestion < length - 1
    },
    ableToBack (): boolean {
      return this.currentQuestion > 0
    },
    showSubmit (): boolean {
      return (
        this.responses.length === this.quiz?.questions.length &&
        this.responses.every((response) => response !== undefined)
      )
    },
    ableToSubmit (): boolean {
      return (
        this.responses.length === this.quiz?.questions.length &&
        this.responses.every((response: number | undefined) => response !== undefined) &&
        this.name !== '' &&
        (!EMAIL_ENABLED || (this.email !== '' &&
        this.email.includes('@')))
      )
    },
    currentQuestionData (): {
    question: string;
    answers: string[];
    } | undefined {
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
<style>
.bodoni-moda {
  font-family: "Bodoni Moda", serif;
  font-optical-sizing: auto;
  /* font-weight: <weight>; */
  font-style: normal;
}

.selectors {
  margin-top: 2px;
}

/**
align children to the left
 */
.selectorList {
  margin-top: 10px;

}

.selectors > label {
  margin-left: 10px;
}
</style>
