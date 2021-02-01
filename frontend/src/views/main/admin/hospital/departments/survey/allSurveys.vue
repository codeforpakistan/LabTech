import { Component, Vue } from 'vue-property-decorator';
<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Survey
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" :to="'/main/admin/hospital/' + hospitalId + '/department/' + departmentId + '/survey/create'">Create Survey</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="departmentSurveys">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.questions }}</td>
        <td class="justify-center layout px-0" colspan="2">
          <!-- <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-hospital-department-survey-create', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip> -->
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readDepartmentSurveys } from '@/store/admin/getters';
import { dispatchGetDepartmentSurveys } from '@/store/admin/actions';
import { ISurvey } from '@/interfaces';


@Component
export default class AdminHospitals extends Vue {
  [x: string]: any;
  public departmentId: string = '';
  public hospitalId: string = '';
  public hospitals: ISurvey[] = [];
  public headers = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'Questions',
      sortable: false,
      value: 'questions',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
      colspan: 2,
      align: 'center',
    },
  ];

  public async mounted() {
    let fullPath: any = this.$router.currentRoute.fullPath;
    fullPath = fullPath.split('/');
    this.hospitalId = fullPath[4];
    this.departmentId = this.$router.currentRoute.params.id;
    await dispatchGetDepartmentSurveys(this.$store, parseInt(this.departmentId, 10));
  }

  get departmentSurveys() {
    return readDepartmentSurveys(this.$store);
  }
}
</script>
