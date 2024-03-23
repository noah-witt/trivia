<template>
  <Card class="Trivia bodoni-moda" v-if="quiz != null">
    <template #title>{{ quiz.title }}</template>
    <template #content>
      <br />
      <span v-if="quiz">
        <Card
          v-for="(question, index) of quiz.questions"
          :key="`question-${index}`"
          class="question-card"
        >
          <template #title>{{ question.question }}</template>
          <template #content>
            <p>
              <span
                v-for="(answer, aIndex) of question.answers"
                :key="`answer-${aIndex}`"
              >
                <InlineMessage :severity="aIndex==question.correct?'success':'secondary'">{{ answer }}</InlineMessage>
                <br/>
                <br/>
              </span>
            </p>
          </template>
        </Card>
      </span>
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
import Card from 'primevue/card'
import InlineMessage from 'primevue/inlinemessage'

interface Question {
  question: string;
  answers: string[];
  correct: number;
}

interface Quiz {
  key: string;
  title: string;
  questions: Question[];
}

export default defineComponent({
  name: 'TriviaKey',
  data () {
    return {
      quiz: null as null | Quiz
    }
  },
  components: {
    Card,
    InlineMessage
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

.question-card {
  margin-top: 10px;
  width: 75%;
  /* Center self */
  margin-left: auto;
  margin-right: auto;
}
</style>
