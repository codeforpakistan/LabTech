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
            <div v-for="eachQuestion in questions" :key="eachQuestion.id">
              <v-text-field label="Question" v-model="eachQuestion.question" required></v-text-field>
              <v-text-field label="Question Alias" v-model="eachQuestion.alias" required></v-text-field>
              <v-text-field label="Question Weightage" v-model="eachQuestion.weightage" type="number" required></v-text-field>
              <v-text-field label="Sub Question" v-model="eachQuestion.sub_questions[0].question"></v-text-field>
              <v-text-field label="Sub Question Alias" v-model="eachQuestion.sub_questions[0].alias"></v-text-field>
              <v-text-field label="Sub Question Weightage" v-model="eachQuestion.sub_questions[0].weightage" type="number"></v-text-field>
            </div>
          </v-form>
          <v-btn @click="addQuestion">Add New Question</v-btn>
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
import { dispatchGetDepartmentSurveys, dispatchCreateDepartmentSurvey } from '@/store/admin/actions';

@Component
export default class CreateHospitalDepartment extends Vue {
  public valid = false;
  public id: any;
  public name: string = '';
  public questions: any = [];
  private hospitalId: string = '';
  private departmentId: string = '';
  private sampleQuestion: any = {
    id: 1,
    question: '',
    alias: '',
    weightage: null,
    sub_questions: [{
      question: '',
      alias: '',
      weightage: null,
    }],
  };
  public async mounted() {
    let fullPath: any = this.$router.currentRoute.fullPath;
    fullPath = fullPath.split('/');
    this.hospitalId = fullPath[4];
    this.departmentId = this.$router.currentRoute.params.id;
    await dispatchGetDepartmentSurveys(this.$store, parseInt(this.departmentId, 10));
    this.questions.push(JSON.parse(JSON.stringify(this.sampleQuestion)));
    this.reset();
  }

  public reset() {
    this.name = '';
    this.questions = [];
    this.questions.push(JSON.parse(JSON.stringify(this.sampleQuestion)));
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public addQuestion() {
    if (this.questions[this.questions.length - 1].question) {
      const anotherQuestion: any = JSON.parse(JSON.stringify(this.sampleQuestion));
      anotherQuestion.id++;
      this.questions.push(anotherQuestion);
    }
  }

  public async submit() {
    const updatedSurvey: ISurveyCreate = {
      name: this.name,
      owner_id: 1,
      department_id: parseInt(this.departmentId, 10),
      create_date: new Date(),
      questions: this.questions,
    };
    await dispatchCreateDepartmentSurvey(this.$store, updatedSurvey);
    this.$router.push(`/main/admin/hospital/${this.hospitalId}/department/${this.departmentId}`);
  }
}
</script>
