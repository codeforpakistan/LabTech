<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Survey</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Name" v-model="name" required></v-text-field>
            <div v-for="(eachQuestion, index) in questions" :key="eachQuestion.q_id" class="mt-3">
              <div v-if="eachQuestion">
                <v-text-field label="Question" v-model="eachQuestion.question" required></v-text-field>
                <v-text-field label="Question Alias" v-model="eachQuestion.alias" required></v-text-field>
                <v-select
                  v-model="eachQuestion.weightage"
                  :items="options"
                  item-text="name"
                  item-value="id"
                  label="Question Weightage"
                  persistent-hint
                  return-object
                  single-line
                  clearable
                  required
                ></v-select>
                <div v-for="eachSubQuestion in eachQuestion.sub_questions" :key="eachSubQuestion.s_q_id" class="mt-4">
                  <v-text-field label="Sub Question" v-model="eachSubQuestion.question"></v-text-field>
                  <v-text-field label="Sub Question Alias" v-model="eachSubQuestion.alias"></v-text-field>
                  <v-select
                    v-model="eachSubQuestion.weightage"
                    :items="options"
                    item-text="name"
                    item-value="id"
                    label="Sub Question Weightage"
                    persistent-hint
                    return-object
                    single-line
                    clearable
                    required
                  ></v-select>
                </div>
              </div>
              <v-btn @click="addNewSubQuestion(index)" class="mb-3">Add New Sub Question</v-btn>
            </div>
          </v-form>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="addQuestion" class="text-right">Add New Question</v-btn>
          </v-card-actions>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  ISurveyCreate,
} from '@/interfaces';
import { dispatchGetDepartmentSurvey, dispatchCreateDepartmentSurvey } from '@/store/admin/actions';

@Component
export default class CreateHospitalDepartment extends Vue {
  public valid = false;
  public id: any;
  public name: string = '';
  public questions: any = [];
  private options: any  = [{ id: 2, name: 'HIGH'}, { id: 3, name: 'CRITICAL'}, { id: 1, name: 'LOW' }];
  private hospitalId: string = '';
  private departmentId: number = -1;
  private sampleQuestion: any = {
    q_id: 1,
    question: '',
    alias: '',
    weightage: null,
    sub_questions: [{
      s_q_id: 1,
      question: '',
      alias: '',
      weightage: null,
    }],
  };

  getIdsManualy() {
    let fullPath: any = this.$router.currentRoute.fullPath;
    fullPath = fullPath.split('/');
    if (fullPath[4]) {
      this.hospitalId = fullPath[4];
    }
    if (fullPath[6]) {
      this.departmentId = parseInt(fullPath[6], 10);
    }
  }

  public async mounted() {
    if (!this.$router.currentRoute.params.departmentId) {
      this.getIdsManualy();
    } else {
      this.hospitalId = this.$router.currentRoute.params.hospitalId;
      this.departmentId = parseInt(this.$router.currentRoute.params.departmentId, 10);
    }
    this.id = this.departmentId;
    await dispatchGetDepartmentSurvey(this.$store, this.id);
    this.reset();
  }

  private reset() {
    this.name = '';
    this.questions = [];
    this.questions.push(JSON.parse(JSON.stringify(this.sampleQuestion)));
    this.$validator.reset();
  }

  private cancel() {
    this.$router.back();
  }

  private addQuestion() {
    if (this.questions[this.questions.length - 1].question) {
      const anotherQuestion: any = JSON.parse(JSON.stringify(this.sampleQuestion));
      anotherQuestion.q_id++;
      this.questions.push(anotherQuestion);
    }
  }

  private addNewSubQuestion(index) {
     if (this.questions[index].sub_questions[this.questions[index].sub_questions.length - 1].question) {
      const anotherSubQuestion: any =
       JSON.parse(JSON.stringify(this.questions[index].sub_questions[this.questions[index].sub_questions.length - 1]));
      anotherSubQuestion.s_q_id++;
      anotherSubQuestion.question = '';
      anotherSubQuestion.weightage = '';
      anotherSubQuestion.alias = '';
      this.questions[index].sub_questions.push(anotherSubQuestion);
    }
  }

  private iterate = (obj) => {
    Object.keys(obj).forEach(key => {
      if (key === 'weightage') {
        obj[key] = obj[key].id
      }
      if (typeof obj[key] === 'object') {
          this.iterate(obj[key])
      }
    });
    return obj;
  } 


  private async submit() {
    this.questions = this.iterate(this.questions);
    console.log(this.questions, 'this.questions')
    const updatedSurvey: ISurveyCreate = {
      name: this.name,
      owner_id: 1,
      department_id: this.departmentId,
      create_date: new Date(),
      questions: this.questions,
    };
    await dispatchCreateDepartmentSurvey(this.$store, updatedSurvey);
    this.$router.push(`/main/admin/hospital/${this.hospitalId}/department/${this.departmentId}/all`);
  }
}
</script>
