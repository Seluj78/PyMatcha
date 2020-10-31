/* eslint-disable max-len */
import jwtDecode from 'jwt-decode';
import Axios from 'axios';
import router from '@/router';

export const setAccessToken = (token) => (localStorage.setItem(process.env.VUE_APP_ACCESS_TOKEN, token));
export const setRefreshToken = (token) => (localStorage.setItem(process.env.VUE_APP_REFRESH_TOKEN, token));

export const getAccessToken = () => (localStorage.getItem(process.env.VUE_APP_ACCESS_TOKEN));
export const getRefreshToken = () => (localStorage.getItem(process.env.VUE_APP_REFRESH_TOKEN));

export const tokenIsValid = (token) => {
  try {
    const { exp } = jwtDecode(token);
    return (Date.now() < exp * 1000);
  } catch (error) {
    return false;
  }
};

export const renewAccessToken = async () => {
  if (getRefreshToken()) {
    try {
      const response = await Axios.post('/auth/refresh', {});
      localStorage.setItem('matchaAccessToken', response.data.access_token);
    } catch (error) {
      await router.push('/accounts/signout');
    }
  }
};

export const handleAccessTokenExpiration = async () => {
  const accessToken = getAccessToken();
  if (accessToken && !tokenIsValid(accessToken)) {
    await renewAccessToken();
  }
};
