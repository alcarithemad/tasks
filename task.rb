require 'rtasklib'
require 'sinatra'
require 'slim'
require 'stylus'
require 'stylus/tilt'

tw = Rtasklib::TW.new('~/.task')

# do some stuff with the task database
# available commands are documented in the Controller class

tasks = tw.all
#=> returns an array of TaskModels

#tasks.first.description
#=> "An example task"

#tasks[-1].due
#=> #<DateTime: 2015-03-16T17:48:23+00:00 ((2457098j,64103s,0n),+0s,2299161j)>

#tw.some(ids: [1..5, 10]).size
#=> 6

#tw.done!(ids: 5)

#tw.some(ids: [1..5, 10]).size
#=> 5

#tw.get_uda_names
#=> ["author", "estimate"]
#

puts tasks[0].description

get "/" do
	slim :index
end

get "/main.css" do
	stylus :main
end

#task.sync!
