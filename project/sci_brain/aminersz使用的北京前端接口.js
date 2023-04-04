  userLogin: `${baseURL}/auth/signin`,
  userLogout: `${baseURL}/auth/signout`,
  signup: `${baseURL}/auth/signup`,
  checkAminerEmail: `${baseURL}/user/check/:email`,
  updatePassword: `${baseURL}/auth/update/passwd`,
  forgot: `${baseURL}/auth/update/forgot`,
  // 重置密码
  retrieve: `${baseURL}/auth/update/token`,
  // search
  searchPersonAgg: `${baseURL}/search/person/agg`,
  searchPersonInBase: `${baseURL}/search/roster/:ebid/experts/advanced`,
  // searchPersonInBaseAgg: `${baseURL}/search/roster/:ebid/experts/advanced/agg`,
  allPersonInBase: `${baseURL}/roster/:ebid/offset/:offset/size/:size`,
  allPersonInBaseWithSort: `${baseURL}/roster/:ebid/order-by/:sort/offset/:offset/size/:size`,
  // search suggest
  searchSuggest: `${baseURL}/search/suggest/gen/:query`,
  // misc services
  translateTerm: `${baseURL}/abbreviation/mapping/:term`,
  // person */
  personProfile: `${baseURL}/person/summary/:id`,
  personEmailImg: `${baseURL}/person/email/i/`,
  personEmailStr: `${baseURL}/person/email/s/:id`,
  getEmailCrImage: `${baseURL}/person/email-cr/i/`,
  listPersonByIds: `${baseURL}/person/batch-list`,
  getActivityAvgScoresByPersonId: `${baseURL}/person/activity/:id/indices`,
  batchGetActivityCompareScoresByPersonId: `${baseURL}/person/activity/:ids/batch/indices`,
  // interests vis data
  interests: `${baseURL}/person/interests/:id`, // 这个是vis图中单独调用的。和人下面的可能不一样.
  // publications */
  pubList: `${baseURL}/person/pubs/:id/all/year/:offset/:size`,
  // vote
  votePersonInSomeTopicById: `${baseURL}/topic/person/vote/:oper/:aid/id/:tid`,
  unvotePersonInSomeTopicById: `${baseURL}/topic/person/vote/:aid/id/:tid`,
  getToBProfileByAid: `${baseURL}/2b/profile/:src/aid/:id`,
  getExpertBase: `${baseURL}/roster/list/:type/offset/:offset/size/:size`,
  addExpertBaseApi: `${baseURL}/roster`,
  deleteExpertBaseApi: `${baseURL}/roster/:rid`,
  getExpertDetailList: `${baseURL}/roster/:ebid/order-by/h_index/offset/:offset/size/:size`,
  invokeRoster: `${baseURL}/roster/:id/members/u`,
      UploadFile: `${nextAPIURLOnlineProduction}/magic`,