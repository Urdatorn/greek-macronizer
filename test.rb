$LOAD_PATH.unshift(File.expand_path('../ifthimos', __FILE__))

puts $LOAD_PATH

#require '/opt/homebrew/lib/ruby/gems/3.3.0/gems/tinycus-1.1.0/tinycus'
require './tinycus-1.1.0/tinycus'
require './ifthimos/ifthimos' # require expects a .rb file

#g = GreekGenos.new('classical')
#pos = Ifthimos::Pos.new('v3piia---') # 3rd person plural, imperfect indicative active
#stem = Ifthimos::Mows.new("εἰσηγ",g,[],pos:pos,tailless:true)
#h = Ifthimos::Inflect.do(stem,pos)
#print h['inflected'],"\n" # prints [εἰσ-ῆγον]