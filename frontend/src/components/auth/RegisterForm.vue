<script setup>
import {
  requiredValidator,
  emailValidator,
  passwordValidator,
  confirmedValidator
} from '@/utils/validators'
import { ref } from 'vue'
import AlertNotification from '../common/AlertNotification.vue'
import { supabase, formActionDefault } from '../../utils/supabase.js'
import { useRouter } from 'vue-router'

const visible = ref(false)
const isVisible = ref(false)
const refVForm = ref()

const router = useRouter()

const FormDataDefault = {
  username: '',
  email: '',
  password: '',
  passwordConfirmation: '',
  profile_pic:
    'https://bvflfwricxabodytryee.supabase.co/storage/v1/object/public/profile/public/profile-default.png'
}

const formData = ref({
  ...FormDataDefault
})

const formAction = ref({
  ...formActionDefault
})

const onSubmit = async () => {
  formAction.value = { ...formActionDefault }
  formAction.value.formProcess = true

  const { data, error } = await supabase.auth.signUp({
    email: formData.value.email,
    password: formData.value.password,
    options: {
      data: {
        username: formData.value.username,
        profile_pic: formData.value.profile_pic
      }
    }
  })

  if (error) {
    console.error(error)

    formAction.value.formErrorMessage = error.message
    formAction.value.formStatus = error.status
  } else if (data) {
    console.log(data)

    formAction.value.formSuccessMessage =
      'Please Verify your Email to Login'

    setTimeout(() => {
      router.replace('/login')
    }, 5000)
  }

  refVForm.value?.reset()
  formAction.value.formProcess = false
}

const onFormSubmit = () => {
  refVForm.value?.validate().then(({ valid }) => {
    if (valid) onSubmit()
  })
}
</script>

<template>
  <AlertNotification
    :form-success-message="formAction.formSuccessMessage"
    :form-error-message="formAction.formErrorMessage"
  />

  <v-form
    ref="refVForm"
    fast-fail
    @submit.prevent="onFormSubmit"
  >

    <!-- USERNAME -->
    <v-text-field
      v-model="formData.username"
      label="Username in Chess.com"
      prepend-inner-icon="mdi-account-outline"
      :rules="[requiredValidator]"
      variant="outlined"
      density="comfortable"
      color="orange-darken-1"
      rounded="lg"
      class="mb-3"
    />

    <!-- EMAIL -->
    <v-text-field
      v-model="formData.email"
      label="Email address"
      prepend-inner-icon="mdi-email-outline"
      :rules="[requiredValidator, emailValidator]"
      variant="outlined"
      density="comfortable"
      color="orange-darken-1"
      rounded="lg"
      class="mb-3"
    />

    <!-- PASSWORD -->
    <v-text-field
      v-model="formData.password"
      label="Password"
      prepend-inner-icon="mdi-lock-outline"
      :append-inner-icon="
        visible ? 'mdi-eye-off' : 'mdi-eye'
      "
      :type="visible ? 'text' : 'password'"
      :rules="[requiredValidator, passwordValidator]"
      variant="outlined"
      density="comfortable"
      color="orange-darken-1"
      rounded="lg"
      class="mb-3"
      @click:append-inner="visible = !visible"
    />

    <!-- PASSWORD CONFIRMATION -->
    <v-text-field
      v-model="formData.passwordConfirmation"
      label="Confirm password"
      prepend-inner-icon="mdi-lock-check-outline"
      :append-inner-icon="
        isVisible ? 'mdi-eye-off' : 'mdi-eye'
      "
      :type="isVisible ? 'text' : 'password'"
      :rules="[
        requiredValidator,
        confirmedValidator(
          formData.passwordConfirmation,
          formData.password
        )
      ]"
      variant="outlined"
      density="comfortable"
      color="orange-darken-1"
      rounded="lg"
      class="mb-5"
      @click:append-inner="isVisible = !isVisible"
    />

    <!-- REGISTER -->
    <v-btn
      type="submit"
      block
      size="large"
      rounded="lg"
      color="orange-darken-1"
      class="font-weight-bold text-none"
      :loading="formAction.formProcess"
      :disabled="formAction.formProcess"
    >
      Create Account
      <v-icon end>
        mdi-arrow-right
      </v-icon>
    </v-btn>

  </v-form>
</template>