<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create User</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field
              label="Full Name"
              v-model="fullName"
              required
            ></v-text-field>
            <v-text-field
              label="E-mail"
              type="email"
              v-model="email"
              v-validate="'required|email'"
              data-vv-name="email"
              :error-messages="errors.collect('email')"
              required
            ></v-text-field>
            <div class="subheading secondary--text text--lighten-2">
              User is superuser
              <span v-if="isSuperuser">(currently is a superuser)</span
              ><span v-else>(currently is not a superuser)</span>
            </div>
            <v-checkbox label="Is Superuser" v-model="isSuperuser"></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">
              User is active <span v-if="isActive">(currently active)</span
              ><span v-else>(currently not active)</span>
            </div>
            <v-checkbox label="Is Active" v-model="isActive"></v-checkbox>
            <v-layout align-center>
              <v-flex>
                <v-text-field
                  type="password"
                  ref="password"
                  label="Set Password"
                  data-vv-name="password"
                  data-vv-delay="100"
                  v-validate="{ required: true }"
                  v-model="password1"
                  :error-messages="errors.first('password')"
                >
                </v-text-field>
                <v-text-field
                  type="password"
                  label="Confirm Password"
                  data-vv-name="password_confirmation"
                  data-vv-delay="100"
                  data-vv-as="password"
                  v-validate="{ required: true, confirmed: 'password' }"
                  v-model="password2"
                  :error-messages="errors.first('password_confirmation')"
                >
                </v-text-field>
              </v-flex>
            </v-layout>
            <div class="mt-3">
              <v-label>Allowed Modules</v-label>
              <!-- <v-layout row wrap>
                <v-flex v-for="(category, index) in types" :key="types[index].text" xs6>
                  <v-checkbox
                    light
                    :label="category.text"
                    v-model="category.selected"
                  >
                  </v-checkbox>
                </v-flex>
              </v-layout> -->
              <v-select
                v-model="selectedHospitals"
                :items="hospitals"
                item-text="name"
                item-value="id"
                label="Select Allowed Modules"
                persistent-hint
                return-object
                single-line
                clearable
                multiple
              ></v-select>
            </div>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid"> Save </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IHospital, IUserProfileCreate } from '@/interfaces';
import {
  dispatchGetUsers,
  dispatchCreateUser,
  dispatchGetHospitals,
} from '@/store/admin/actions';
import { readAdminHospital } from '@/store/admin/getters';

@Component
export default class CreateUser extends Vue {
  public selectedHospitals: any = [];
  public valid = false;
  public fullName: string = '';
  public email: string = '';
  public isActive: boolean = true;
  public isSuperuser: boolean = false;
  public setPassword = false;
  public password1: string = '';
  public password2: string = '';
  public types = [
    { text: 'HOSPITAL', value: 'HOSPITAL', selected: false },
    { text: 'BHU', value: 'BHU', selected: false },
    { text: 'OTHER', value: 'OTHER', selected: false },
  ];

  public async mounted() {
    await dispatchGetUsers(this.$store);
    await dispatchGetHospitals(this.$store);
    this.reset();
  }

  public reset() {
    this.password1 = '';
    this.password2 = '';
    this.fullName = '';
    this.email = '';
    this.isActive = true;
    this.isSuperuser = false;
    this.$validator.reset();
  }

  get hospitals() {
    return readAdminHospital(this.$store);
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      let BHUs: any[] = [];
      let Hospitals: any[] = [];
      let Others: any[] = [];
      const isBHUSelected = this.types.find((each) => each.text === 'BHU' && each.selected === true);
      const isHospitalSelected = this.types.find((each) => each.text === 'HOSPITAL' && each.selected === true);
      const isOtherSelected = this.types.find((each) => each.text === 'OTHER' && each.selected === true);
      if (isBHUSelected) {
        BHUs = this.hospitals.filter((each) => each?.hospital_type === 'BHU');
      }
      if (isHospitalSelected) {
        Hospitals = this.hospitals.filter((each) => each?.hospital_type === 'HOSPITAL');
      }
      if (isOtherSelected) {
        Others = this.hospitals.filter((each) => each?.hospital_type === 'OTHER');
      }
      this.selectedHospitals = [...this.selectedHospitals, ...BHUs, ...Hospitals, ...Others];
      this.selectedHospitals = this.selectedHospitals.filter(
                              (v: any, i: any, a: any) => a.findIndex((t: any) => (t.name === v.name)) === i);
      const updatedProfile: IUserProfileCreate = {
        email: this.email,
        allowed_hospitals: this.selectedHospitals?.map(({ id, name }) => ({
          id,
          name,
        })),
      };
      if (this.fullName) {
        updatedProfile.full_name = this.fullName;
      }
      if (this.email) {
        updatedProfile.email = this.email;
      }
      updatedProfile.is_active = this.isActive;
      updatedProfile.is_superuser = this.isSuperuser;
      updatedProfile.password = this.password1;
      await dispatchCreateUser(this.$store, updatedProfile);
      this.$router.push('/main/admin/users');
    }
  }
}
</script>
