

export default class TransformText {
    constructor() {

    }

    getGenderFromBoolean(genderBoolean) {
        if (genderBoolean === true) {
            return 'Male';
        } else {
            return 'Female';
        }
    }
}