<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit User</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Username</div>
            <div
              class="title primary--text text--darken-2"
              v-if="user"
            >{{user.email}}</div>
            <div
              class="title primary--text text--darken-2"
              v-else
            >-----</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
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
            <div class="subheading secondary--text text--lighten-2">User is superuser <span v-if="isSuperuser">(currently is a superuser)</span><span v-else>(currently is not a superuser)</span></div>
            <v-checkbox
              label="Is Superuser"
              v-model="isSuperuser"
            ></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">User is active <span v-if="isActive">(currently active)</span><span v-else>(currently not active)</span></div>
            <v-checkbox
              label="Is Active"
              v-model="isActive"
            ></v-checkbox>
            <v-layout align-center>
              <v-flex shrink>
                <v-checkbox
                  v-model="setPassword"
                  class="mr-2"
                ></v-checkbox>
              </v-flex>
              <v-flex>
                <v-text-field
                  :disabled="!setPassword"
                  type="password"
                  ref="password"
                  label="Set Password"
                  data-vv-name="password"
                  data-vv-delay="100"
                  v-validate="{required: setPassword}"
                  v-model="password1"
                  :error-messages="errors.first('password')"
                >
                </v-text-field>
                <v-text-field
                  v-show="setPassword"
                  type="password"
                  label="Confirm Password"
                  data-vv-name="password_confirmation"
                  data-vv-delay="100"
                  data-vv-as="password"
                  v-validate="{required: setPassword, confirmed: 'password'}"
                  v-model="password2"
                  :error-messages="errors.first('password_confirmation')"
                >
                </v-text-field>
              </v-flex>
            </v-layout>
            <div class="mt-3">
              <v-label>Allowed Hospitals</v-label>
              <v-layout row wrap>
                <v-flex v-for="(category, index) in types" :key="types[index].text" xs6>
                  <v-checkbox
                    light
                    :label="category.text"
                    v-model="category.selected"
                  >
                  </v-checkbox>
                </v-flex>
              </v-layout>
              <v-select
                v-model="selectedHospitals"
                :items="hospitals"
                item-text="name"
                item-value="id"
                label="Select Allowed Hospitals"
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
        <v-btn
          @click="submit"
          :disabled="!valid"
        >
          Update
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IUserProfile, IUserProfileUpdate } from '@/interfaces';
import { dispatchGetUsers, dispatchUpdateUser, dispatchGetHospitals } from '@/store/admin/actions';
import { readAdminOneUser, readAdminHospital } from '@/store/admin/getters';

@Component
export default class EditUser extends Vue {
  public selectedHospitals: any = [];
  public valid = true;
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
    this.setPassword = false;
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
    if (this.user) {
      this.fullName = this.user.full_name;
      this.email = this.user.email;
      this.isActive = this.user.is_active;
      this.isSuperuser = this.user.is_superuser;
      this.selectedHospitals = (this.user?.allowed_hospitals?.map(({ id, name }) => ({ id, name}))) || [];
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileUpdate = {};
      let BHUs: any[] = [];
      let Hospitals: any[] = [];
      let Others: any[] = [];
      if (this.fullName) {
        updatedProfile.full_name = this.fullName;
      }
      if (this.selectedHospitals && this.selectedHospitals.length > 0) {
        updatedProfile.allowed_hospitals = this.selectedHospitals?.map(({ id, name }) => ({ id, name}));
      }
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
      if (this.selectedHospitals && this.selectedHospitals.length > 0) {
        updatedProfile.allowed_hospitals = this.selectedHospitals;
      }                        
      if (this.email) {
        updatedProfile.email = this.email;
      }
      updatedProfile.is_active = this.isActive;
      updatedProfile.is_superuser = this.isSuperuser;
      if (this.setPassword) {
        updatedProfile.password = this.password1;
      }
      await dispatchUpdateUser(this.$store, { id: this.user!.id, user: updatedProfile });
      this.$router.push('/main/admin/users');
    }
  }

  get user() {
    return readAdminOneUser(this.$store)(+this.$router.currentRoute.params.id);
  }

  get hospitals() {
    return readAdminHospital(this.$store);
  }

  trySpread(object) {
    let array;
    try {
      array = [...object];
      console.log('No error', array);
    } catch(error) {
      console.log('error', error);
    }
    return
  }

}
</script>
