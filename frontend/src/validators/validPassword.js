function validPassword(password) {
  if (password.length > 16) {
    return true;
  }
  return !password.match(/^[a-z]+$/);
}

export default validPassword;
