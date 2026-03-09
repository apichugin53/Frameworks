.photo {
  border: 1px solid transparent;
  border-radius: 10px;
  width: 100%;
}

.logo {
  min-width: 36px;
}

.form-max-w {
    max-width: 450px;
}

.form-max-w-2 {
    max-width: 900px;
}

.form-min-w {
  min-width: 300px;
}

.breed-card {
  white-space: nowrap;
  text-overflow:ellipsis;
  overflow: hidden;
}

.dog-card {
  width: 240px;
  height: 240px;
}

.dog-card-img {
  max-height: 140px;
  height: 100%;
}

.dogs_list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  /*justify-content: space-around;*/
  gap: 1rem;
}

.dog-detail-img {
  max-width: 360px;
  max-height: 360px;
  width: 360px;
  height: auto;
}

.error-wrapper {
  display: table;
  width: 100%;
}

.error-wrapper > .errorlist {
  display: table-footer-group;
}

ul.errorlist {
  margin: 0;
  padding: 0;
}

ul.errorlist li {
  list-style-type: none;
  color: red;
}
