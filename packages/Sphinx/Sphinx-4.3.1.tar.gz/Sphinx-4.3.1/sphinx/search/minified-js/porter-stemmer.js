PorterStemmer=function(){var r=new BaseStemmer;var e=[["s",-1,3],["ies",0,2],["sses",0,1],["ss",0,-1]];var i=[["",-1,3],["bb",0,2],["dd",0,2],["ff",0,2],["gg",0,2],["bl",0,1],["mm",0,2],["nn",0,2],["pp",0,2],["rr",0,2],["at",0,1],["tt",0,2],["iz",0,1]];var s=[["ed",-1,2],["eed",0,1],["ing",-1,2]];var a=[["anci",-1,3],["enci",-1,2],["abli",-1,4],["eli",-1,6],["alli",-1,9],["ousli",-1,11],["entli",-1,5],["aliti",-1,9],["biliti",-1,13],["iviti",-1,12],["tional",-1,1],["ational",10,8],["alism",-1,9],["ation",-1,8],["ization",13,7],["izer",-1,7],["ator",-1,8],["iveness",-1,12],["fulness",-1,10],["ousness",-1,11]];var u=[["icate",-1,2],["ative",-1,3],["alize",-1,1],["iciti",-1,2],["ical",-1,2],["ful",-1,3],["ness",-1,3]];var t=[["ic",-1,1],["ance",-1,1],["ence",-1,1],["able",-1,1],["ible",-1,1],["ate",-1,1],["ive",-1,1],["ize",-1,1],["iti",-1,1],["al",-1,1],["ism",-1,1],["ion",-1,2],["er",-1,1],["ous",-1,1],["ant",-1,1],["ent",-1,1],["ment",15,1],["ement",16,1],["ou",-1,1]];var c=[17,65,16,1];var f=[1,17,65,208,1];var l=false;var o=0;var n=0;function b(){if(!r.out_grouping_b(f,89,121)){return false}if(!r.in_grouping_b(c,97,121)){return false}if(!r.out_grouping_b(c,97,121)){return false}return true}function m(){if(!(n<=r.cursor)){return false}return true}function _(){if(!(o<=r.cursor)){return false}return true}function k(){var i;r.ket=r.cursor;i=r.find_among_b(e);if(i==0){return false}r.bra=r.cursor;switch(i){case 1:if(!r.slice_from("ss")){return false}break;case 2:if(!r.slice_from("i")){return false}break;case 3:if(!r.slice_del()){return false}break}return true}function v(){var e;r.ket=r.cursor;e=r.find_among_b(s);if(e==0){return false}r.bra=r.cursor;switch(e){case 1:if(!m()){return false}if(!r.slice_from("ee")){return false}break;case 2:var a=r.limit-r.cursor;r:while(true){e:{if(!r.in_grouping_b(c,97,121)){break e}break r}if(r.cursor<=r.limit_backward){return false}r.cursor--}r.cursor=r.limit-a;if(!r.slice_del()){return false}var u=r.limit-r.cursor;e=r.find_among_b(i);if(e==0){return false}r.cursor=r.limit-u;switch(e){case 1:{var t=r.cursor;r.insert(r.cursor,r.cursor,"e");r.cursor=t}break;case 2:r.ket=r.cursor;if(r.cursor<=r.limit_backward){return false}r.cursor--;r.bra=r.cursor;if(!r.slice_del()){return false}break;case 3:if(r.cursor!=n){return false}var f=r.limit-r.cursor;if(!b()){return false}r.cursor=r.limit-f;{var l=r.cursor;r.insert(r.cursor,r.cursor,"e");r.cursor=l}break}break}return true}function g(){r.ket=r.cursor;r:{var e=r.limit-r.cursor;e:{if(!r.eq_s_b("y")){break e}break r}r.cursor=r.limit-e;if(!r.eq_s_b("Y")){return false}}r.bra=r.cursor;r:while(true){e:{if(!r.in_grouping_b(c,97,121)){break e}break r}if(r.cursor<=r.limit_backward){return false}r.cursor--}if(!r.slice_from("i")){return false}return true}function d(){var e;r.ket=r.cursor;e=r.find_among_b(a);if(e==0){return false}r.bra=r.cursor;if(!m()){return false}switch(e){case 1:if(!r.slice_from("tion")){return false}break;case 2:if(!r.slice_from("ence")){return false}break;case 3:if(!r.slice_from("ance")){return false}break;case 4:if(!r.slice_from("able")){return false}break;case 5:if(!r.slice_from("ent")){return false}break;case 6:if(!r.slice_from("e")){return false}break;case 7:if(!r.slice_from("ize")){return false}break;case 8:if(!r.slice_from("ate")){return false}break;case 9:if(!r.slice_from("al")){return false}break;case 10:if(!r.slice_from("ful")){return false}break;case 11:if(!r.slice_from("ous")){return false}break;case 12:if(!r.slice_from("ive")){return false}break;case 13:if(!r.slice_from("ble")){return false}break}return true}function w(){var e;r.ket=r.cursor;e=r.find_among_b(u);if(e==0){return false}r.bra=r.cursor;if(!m()){return false}switch(e){case 1:if(!r.slice_from("al")){return false}break;case 2:if(!r.slice_from("ic")){return false}break;case 3:if(!r.slice_del()){return false}break}return true}function h(){var e;r.ket=r.cursor;e=r.find_among_b(t);if(e==0){return false}r.bra=r.cursor;if(!_()){return false}switch(e){case 1:if(!r.slice_del()){return false}break;case 2:r:{var i=r.limit-r.cursor;e:{if(!r.eq_s_b("s")){break e}break r}r.cursor=r.limit-i;if(!r.eq_s_b("t")){return false}}if(!r.slice_del()){return false}break}return true}function p(){r.ket=r.cursor;if(!r.eq_s_b("e")){return false}r.bra=r.cursor;r:{var e=r.limit-r.cursor;e:{if(!_()){break e}break r}r.cursor=r.limit-e;if(!m()){return false}{var i=r.limit-r.cursor;e:{if(!b()){break e}return false}r.cursor=r.limit-i}}if(!r.slice_del()){return false}return true}function q(){r.ket=r.cursor;if(!r.eq_s_b("l")){return false}r.bra=r.cursor;if(!_()){return false}if(!r.eq_s_b("l")){return false}if(!r.slice_del()){return false}return true}this.stem=function(){l=false;var e=r.cursor;r:{r.bra=r.cursor;if(!r.eq_s("y")){break r}r.ket=r.cursor;if(!r.slice_from("Y")){return false}l=true}r.cursor=e;var i=r.cursor;r:{while(true){var s=r.cursor;e:{i:while(true){var a=r.cursor;s:{if(!r.in_grouping(c,97,121)){break s}r.bra=r.cursor;if(!r.eq_s("y")){break s}r.ket=r.cursor;r.cursor=a;break i}r.cursor=a;if(r.cursor>=r.limit){break e}r.cursor++}if(!r.slice_from("Y")){return false}l=true;continue}r.cursor=s;break}}r.cursor=i;n=r.limit;o=r.limit;var u=r.cursor;r:{e:while(true){i:{if(!r.in_grouping(c,97,121)){break i}break e}if(r.cursor>=r.limit){break r}r.cursor++}e:while(true){i:{if(!r.out_grouping(c,97,121)){break i}break e}if(r.cursor>=r.limit){break r}r.cursor++}n=r.cursor;e:while(true){i:{if(!r.in_grouping(c,97,121)){break i}break e}if(r.cursor>=r.limit){break r}r.cursor++}e:while(true){i:{if(!r.out_grouping(c,97,121)){break i}break e}if(r.cursor>=r.limit){break r}r.cursor++}o=r.cursor}r.cursor=u;r.limit_backward=r.cursor;r.cursor=r.limit;var t=r.limit-r.cursor;k();r.cursor=r.limit-t;var f=r.limit-r.cursor;v();r.cursor=r.limit-f;var b=r.limit-r.cursor;g();r.cursor=r.limit-b;var m=r.limit-r.cursor;d();r.cursor=r.limit-m;var _=r.limit-r.cursor;w();r.cursor=r.limit-_;var z=r.limit-r.cursor;h();r.cursor=r.limit-z;var y=r.limit-r.cursor;p();r.cursor=r.limit-y;var Y=r.limit-r.cursor;q();r.cursor=r.limit-Y;r.cursor=r.limit_backward;var C=r.cursor;r:{if(!l){break r}while(true){var S=r.cursor;e:{i:while(true){var B=r.cursor;s:{r.bra=r.cursor;if(!r.eq_s("Y")){break s}r.ket=r.cursor;r.cursor=B;break i}r.cursor=B;if(r.cursor>=r.limit){break e}r.cursor++}if(!r.slice_from("y")){return false}continue}r.cursor=S;break}}r.cursor=C;return true};this["stemWord"]=function(e){r.setCurrent(e);this.stem();return r.getCurrent()}};