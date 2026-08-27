import { Api } from './client'

export const passwordResetApi = {
  async requestReset(email: string) {
    return Api.request<{ success: boolean; message: string }>('/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
    })
  },

  async confirmPassword(token: string, newPassword: string) {
    return Api.request<{ success: boolean; message: string }>('/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ token, new_password: newPassword }),
    })
  },
}
