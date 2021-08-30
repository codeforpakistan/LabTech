import { Component, Vue } from 'vue-property-decorator';
<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Lab
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/lab/create">Create Lab</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="hospitals">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.address }}</td>
        <td>{{ dateToString(props.item.created_date) }}</td>
        <!-- <td>{{ props.item.lat }}</td>
        <td>{{ props.item.lng }}</td>
        <td>{{ props.item.hospital_type ?  props.item.hospital_type.toUpperCase() : 'OTHER' }}</td> -->
        <td class="justify-center layout px-0" colspan="2">
          <v-tooltip top>
            <span>View / Edit Departments</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-hospitals-departments', params: {id: props.item.id}}">
              <v-icon>visibility</v-icon>
            </v-btn>
          </v-tooltip>
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-hospitals-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
           <v-tooltip top>
            <span>Delete</span>
            <v-btn slot="activator" flat  v-on:click.native="deleteHospital(props.item.id, props.item.name)">
              <v-icon>delete</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readAdminHospital } from '@/store/admin/getters';
import { readUserProfile } from '@/store/main/getters';
import { dispatchGetHospitals, dispatchDeleteHospital } from '@/store/admin/actions';


@Component
export default class AdminHospitals extends Vue {
  [x: string]: any;
  public headers = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'Address',
      sortable: true,
      value: 'address',
      align: 'left',
    },
    {
      text: 'Created Date',
      sortable: true,
      value: 'create_date',
      align: 'left',
    },
    // {
    //   text: 'Lattitue',
    //   sortable: true,
    //   value: 'lat',
    //   align: 'left',
    // },
    // {
    //   text: 'Longitude',
    //   sortable: true,
    //   value: 'lng',
    //   align: 'left',
    // },
    // {
    //   text: 'Hospital Type',
    //   sortable: true,
    //   value: 'hospital_type',
    //   align: 'left',
    // },
    {
      text: 'Actions',
      value: 'id',
      colspan: 2,
      align: 'center',
    },
  ];

  public async mounted() {
    await dispatchGetHospitals(this.$store);
  }

  public async deleteHospital(id: number, name: string) {
    if (confirm(`Do you want to delete ${name}, along with indicators and submissions?`)) {
        await dispatchDeleteHospital(this.$store, id);
        await dispatchGetHospitals(this.$store);
    }
  }

  get hospitals() {
    return readAdminHospital(this.$store);
  }

  get userProfile() {
    return readUserProfile(this.$store);
  }

  private dateToString(date) {
   if (!date) {
     return 'N/A';
   }
   date = new Date(date);
   const month = date.getMonth() + 1;
   const day = date.getDate();
   return date.getFullYear() + '-' +
        (month.toString().length === 1 ? '0' + month : month)  +
        '-'  + (day.toString().length === 1 ? '0' + day : day);
  }
}
</script>
