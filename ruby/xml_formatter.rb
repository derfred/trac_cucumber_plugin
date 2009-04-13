require "cucumber"
require 'erb'
begin
  require 'builder'
rescue LoadError
  gem 'builder'
  require 'builder'
end

class XMLFormatter < Cucumber::Ast::Visitor
  def initialize(step_mother, io, options)
    super(step_mother)
    @builder = Builder::XmlMarkup.new(:target => io, :indent => 2)
  end
  
  def visit_features(features)
    @builder.instruct!
    @builder.features do
      super
    end
  end

  def visit_feature(feature)
    @builder.feature(:name => File.basename(feature.file)) do
      super
    end
  end

  def visit_feature_name(name)
    @builder.feature_name name
  end

  def visit_background(background)
    @builder.background do
      super
    end
  end

  def visit_background_name(keyword, name, file_colon_line, source_indent)
    @builder.background_name name
  end

  def visit_feature_element(feature_element)
    @builder.scenario do
      super
    end
  end
  
  def visit_scenario_name(keyword, name, file_colon_line, source_indent)
    @builder.scenario_name name
  end

  def visit_steps(steps)
    @builder.steps do
      super
    end
  end

  def visit_step(step)
    @builder.step do
      super
    end
  end

  def visit_step_name(keyword, step_match, status, source_indent, background)
    @builder.keyword keyword
    @builder.name step_match.format_args(lambda{|a| a})
    @builder.status status.to_s
  end

  def visit_py_string(string, status=nil)
    @builder.multiline_arg string
  end

  def visit_exception(exception, status)
    @builder.exception format_exception(exception)
  end

  private

    def format_exception(exception)
      (["#{exception.message} (#{exception.class})"] + exception.backtrace).join("\n")
    end
end
